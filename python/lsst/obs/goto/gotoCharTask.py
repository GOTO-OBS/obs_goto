from lsst.pipe.tasks.characterizeImage import CharacterizeImageTask, CharacterizeImageConfig
import lsst.pex.config as pexConfig
import lsst.afw.table as afwTable
from lsst.afw.table import IdFactory, SourceTable
from lsst.meas.extensions.astrometryNet import LoadAstrometryNetObjectsTask
from lsst.meas.astrom import AstrometryTask
import lsst.pipe.base as pipeBase

class GotoCharacterizeImageConfig(CharacterizeImageConfig):
    doEarlyAstrometry = pexConfig.Field(
        dtype=bool,
        default=False,
        doc="Perform astrometry on raw frame (only needed if raw frame does not come with a WCS solution",
    )

    astromRefObjLoader = pexConfig.ConfigurableField(
                target=LoadAstrometryNetObjectsTask,
                doc="reference object loader for astrometric calibration",
    )
    
    astrometry = pexConfig.ConfigurableField(
        target = AstrometryTask,
        doc="""Task to obtain an initial WCS should your raw data not come with a WCS solution.""",
    )
            
class GotoCharacterizeImageTask(CharacterizeImageTask):
    ConfigClass = GotoCharacterizeImageConfig

    def __init__(self, butler=None, astromRefObjLoader=None, schema=None, **kwargs):
        super(GotoCharacterizeImageTask, self).__init__(**kwargs)
        self.makeSubtask('astromRefObjLoader', butler=butler)
        self.makeSubtask("astrometry", refObjLoader=astromRefObjLoader,
                         schema=self.schema)
        
    def run(self, dataRef, exposure=None, background=None, doUnpersist=True,
            doPsf=True, doApCorr=True, doWrite=True, doCalc=True):

        self.log.info("gotoCharTask Processing %s" % (dataRef.dataId))

        if doUnpersist:
            if exposure is not None or background is not None:
                raise RuntimeError("doUnpersist true; exposure and background must be None")
            exposure = dataRef.get("postISRCCD", immediate=True)
        elif exposure is None:
            raise RuntimeError("doUnpersist false; exposure must be provided")
        
        exposureIdInfo = dataRef.get("expIdInfo")

        if not exposure.hasPsf():
            self.log.warn("Using SimplePsf for astrometry source detection")
            self.installSimplePsf.run(exposure=exposure)

        #Repair cosmic rays
        self.repair.run(exposure=exposure, keepCRs=True)
            
        # subtract an initial estimate of background level
        background = self.background.run(exposure).background

        #Table schema needs to be set up prior to detection:
        sourceIdFactory = IdFactory.makeSource(exposureIdInfo.expId,
                                               exposureIdInfo.unusedBits)
        table = SourceTable.make(self.schema, sourceIdFactory)
        table.setMetadata(self.algMetadata)

        #Perform detection
        sourceCat = self.detection.run(table=table, exposure=exposure,
                                       doSmooth=True).sources

        #Perform measurement
        self.measurement.run(
            measCat=sourceCat,
            exposure=exposure,
            exposureId=exposureIdInfo.expId)
        
        if self.config.doEarlyAstrometry:
            astromRes = self.astrometry.run(exposure=exposure,
                                            sourceCat=sourceCat)

        measPsfRes = pipeBase.Struct(cellSet=None)
        if doPsf and self.config.doMeasurePsf:
            if self.measurePsf.usesMatches:
                matches = self.ref_match.loadAndMatch(exposure=exposure, sourceCat=sourceCat).matches
            else:
                matches = None        
            psfIterations = self.config.psfIterations if self.config.doMeasurePsf else 1
            for i in range(psfIterations):
                measPsfRes = self.measurePsf.run(exposure=exposure, sources=sourceCat, matches=matches,
                                                 expId=exposureIdInfo.expId)

        # perform final repair with final PSF
        self.repair.run(exposure=exposure)

        if doApCorr and self.config.doApCorr:
            apCorrMap = self.measureApCorr.run(exposure=exposure, catalog=sourceCat).apCorrMap
            exposure.getInfo().setApCorrMap(apCorrMap)
            self.applyApCorr.run(catalog=sourceCat, apCorrMap=exposure.getInfo().getApCorrMap())

        if doCalc:
            self.catalogCalculation.run(sourceCat)
        
        if doWrite and self.config.doWrite:
            dataRef.put(sourceCat, "icSrc")
            if self.config.doWriteExposure:
                dataRef.put(exposure, "icExp")
                dataRef.put(background, "icExpBackground")

        return pipeBase.Struct(
            exposure=exposure,
            sourceCat=sourceCat,
            background=background,
            psfCellSet=measPsfRes.cellSet,
        )
