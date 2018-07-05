#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
import lsst.pex.config as pexConfig
import lsst.pipe.base as pipeBase
import lsst.daf.base as dafBase
import lsst.afw.table as afwTable
from lsst.afw.table import IdFactory, SourceTable
from lsst.obs.base import ExposureIdInfo
from lsst.meas.algorithms import SourceDetectionTask, SubtractBackgroundTask
from lsst.meas.algorithms.installGaussianPsf import InstallGaussianPsfTask
from lsst.meas.extensions.astrometryNet import LoadAstrometryNetObjectsTask
from lsst.meas.astrom import AstrometryTask
from lsst.meas.base import SingleFrameMeasurementTask
                            
__all__ = ["AstrometryConfig", "AstrometryTask"]

class AstrometryConfig(pexConfig.Config):
    """Config for AstrometryTask"""
    detection = pexConfig.ConfigurableField(
                            target=SourceDetectionTask,
                            doc="Detect sources",
    )

    measurement = pexConfig.ConfigurableField(
                target=SingleFrameMeasurementTask,
                doc="Measure sources",
    )
    
    installSimplePsf = pexConfig.ConfigurableField(
        target=InstallGaussianPsfTask,
        doc="Install a simple PSF model",
    )

    background = pexConfig.ConfigurableField(
        target=SubtractBackgroundTask,
        doc="Configuration for initial background estimation",
    )

    astromRefObjLoader = pexConfig.ConfigurableField(
        target=LoadAstrometryNetObjectsTask,
        doc="reference object loader for astrometric calibration",
    )

    astrometry = pexConfig.ConfigurableField(
                target=AstrometryTask,
                doc="Perform astrometric calibration to refine the WCS",
            )
    
    def setDefaults(self):
        pexConfig.Config.setDefaults(self)
                
class AstrometryTask(pipeBase.CmdLineTask):

    ConfigClass = AstrometryConfig
    _DefaultName = "astrometry"
    RunnerClass = pipeBase.ButlerInitializedTaskRunner
    
    def __init__(self, butler=None, astromRefObjLoader=None, **kwargs):
        
        pipeBase.CmdLineTask.__init__(self, **kwargs)
        self.makeSubtask("installSimplePsf")
        self.makeSubtask("background")
        
        self.schema = afwTable.SourceTable.makeMinimalSchema()
        self.makeSubtask('detection', schema=self.schema)
        
        self.algMetadata = dafBase.PropertyList()
        
        self.makeSubtask('measurement', schema=self.schema,
                         algMetadata=self.algMetadata)
        
        if astromRefObjLoader is None:
            self.makeSubtask('astromRefObjLoader', butler=butler)
            astromRefObjLoader = self.astromRefObjLoader
        self.pixelMargin = astromRefObjLoader.config.pixelMargin
        self.makeSubtask("astrometry", refObjLoader=astromRefObjLoader,
                         schema=self.schema)
        
    @pipeBase.timeMethod
    def run(self, dataRef=None, exposure=None):

        if not exposure.hasPsf():
            self.log.warn("Using SimplePsf for astrometry source detection")
            self.installSimplePsf.run(exposure=exposure)

        #Ensure a unique source identifier is allocated:
        #(This isn't actually necessary for this stage)
        butler = dataRef.getButler()
        exposureIdInfo = butler.get('expIdInfo',dataRef.dataId)
        
        #Subtract an initial estimate of the background:
        background = self.background.run(exposure).background

        #Table schema needs to be set up prior to detection:
        sourceIdFactory = IdFactory.makeSource(exposureIdInfo.expId,
                                               exposureIdInfo.unusedBits)
        table = SourceTable.make(self.schema, sourceIdFactory)
        table.setMetadata(self.algMetadata)
        
        #Perform detection
        detRes = self.detection.run(table=table, exposure=exposure,
                                    doSmooth=True)

        sourceCat = detRes.sources
        
        self.measurement.run(
            measCat=sourceCat,
            exposure=exposure,
            exposureId=exposureIdInfo.expId)

        import pdb
        pdb.set_trace()
        astromRes = self.astrometry.run(exposure=exposure,
                                        sourceCat=sourceCat)

        return exposure
