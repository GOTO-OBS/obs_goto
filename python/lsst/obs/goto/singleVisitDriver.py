from lsst.ctrl.pool.parallel import BatchPoolTask, BatchParallelTask
from lsst.ctrl.pool.pool import Pool, NODE
from lsst.pex.config import Config, ConfigurableField
from lsst.pipe.base import ArgumentParser, ConfigDatasetType, TaskRunner, DataIdContainer, ButlerInitializedTaskRunner
from lsst.ip.isr import IsrTask
from .astrometry import AstrometryTask
from lsst.pipe.tasks.warpAndPsfMatch import WarpAndPsfMatchTask
from lsst.pipe.tasks.snapCombine import SnapCombineTask
from lsst.pipe.tasks.characterizeImage import CharacterizeImageTask
from lsst.pipe.tasks.calibrate import CalibrateTask

class RawDataIdContainer(DataIdContainer):
    '''Container Class for raw data; groups all data into a list,
    rather than separate files. The whole list is passed to run()
    in one go, rather than individually, by getTargetList().'''

    def makeDataRefList(self, namespace):
        super(RawDataIdContainer, self).makeDataRefList(namespace)
        visitRefs = []
        for ref in self.refList:
            visitRefs.append(namespace.butler.dataRef(datasetType='visitCoadd_calexp',
                                                      dateObs=ref.dataId['dateObs'],
                                                      filter=ref.dataId['filter'],
                                                      ccd=ref.dataId['ccd'],
                                                      visit=ref.dataId['visit']))
                
class SingleVisitDriverConfig(Config):
    
    isr = ConfigurableField(
        target=IsrTask,
        doc="""Task to perform instrumental signature removal or load a post-ISR image; ISR consists of:
        - assemble raw amplifier images into an exposure with image, variance and mask planes
        - perform bias subtraction, flat fielding, etc.
        - mask known bad pixels
        - provide a preliminary WCS
        """)

    astrometry = ConfigurableField(
        target = AstrometryTask,
        doc="""Task to obtain an initial WCS should your raw data not come with a WCS solution.""")
    
    warp = ConfigurableField(
        target = WarpAndPsfMatchTask,
        doc = """Warps and optionally PSF matches (the latter set to False by default)""")

    snapCombine = ConfigurableField(
        target=SnapCombineTask,
        doc="""Sums two exposures""")

    charImage = ConfigurableField(
        target=CharacterizeImageTask,
        doc="""Task to characterize a coadded visit frame:
            - detect sources, usually at high S/N
            - estimate the background, which is subtracted from the image and returned as field "background"
            - estimate a PSF model, which is added to the exposure
            - interpolate over defects and cosmic rays, updating the image, variance and mask planes
            """)

    calibrate = ConfigurableField(
        target=CalibrateTask,
        doc="""Task to perform astrometric and photometric calibration:
        - refine the WCS in the exposure
        - refine the Calib photometric calibration object in the exposure
        - detect sources, usually at low S/N
        """)

    def setDefaults(self):
        self.snapCombine.doRepair = False
        self.snapCombine.badMaskPlanes = ()
        
class SingleVisitDriverTaskRunner(TaskRunner):
    
    def __init__(self, TaskClass, parsedCmd, doReturnResults=True):
        TaskRunner.__init__(self, TaskClass, parsedCmd, doReturnResults)
        self.butler = parsedCmd.butler
        
    def makeTask(self, parsedCmd=None, args=None):
        if parsedCmd is not None:
            butler = parsedCmd.butler
        elif args is not None:
            dataRef, kwargs = args
            butler = dataRef[0].butlerSubset.butler
        return self.TaskClass(config=self.config, log=self.log, butler=self.butler)
    
    @staticmethod
    def getTargetList(parsedCmd, **kwargs):
        """Passes the data reference list and butler to run()."""
        kwargs["butler"] = parsedCmd.butler
        return [(parsedCmd.id.refList, kwargs), ]

def unpickle(factory, args, kwargs):
    """Unpickle something by calling a factory"""
    return factory(*args, **kwargs)
    
class SingleVisitDriverTask(BatchPoolTask):

    ConfigClass = SingleVisitDriverConfig
    _DefaultName = "singleVisitDriver"
    RunnerClass = SingleVisitDriverTaskRunner    

    def __init__(self, butler=None, *args, **kwargs):
        BatchPoolTask.__init__(self, **kwargs)
        self.butler = butler
        self.makeSubtask("isr")
        self.makeSubtask("astrometry")
        self.makeSubtask("warp")
        self.makeSubtask("snapCombine")
        self.makeSubtask("charImage")
        self.makeSubtask("calibrate", butler=butler)
        
    def __reduce__(self):
        """Pickler"""
        return unpickle, (self.__class__, [], dict(config=self.config, name=self._name,
                                                   parentTask=self._parentTask, log=self.log,
                                                   butler=self.butler))
        
    @classmethod
    def _makeArgumentParser(cls, **kwargs):
        parser = ArgumentParser(name=cls._DefaultName)
        parser.add_id_argument("--id", "raw",
                               level="sensor",
                               help="data ID, e.g. --id visit=12345 ccd=2",
                               ContainerClass=RawDataIdContainer)
        return parser

    def run(self, rawRefList, butler):
        pool = Pool("visits")
        pool.storeSet(butler=butler)

        #Make unique combinations of visit and CCD number:
        #This 4 needs to be replaced by a config parameter.
        visitCcdIdList = set()
        for rawRef in rawRefList:
            visitCcdIdList.add((rawRef.dataId['visit']<<4)+rawRef.dataId['ccd'])
        visitCcdIdList = list(visitCcdIdList)
        
        #Map visits/ccds out to separate nodes:
        pool.map(self.runVisit, visitCcdIdList, rawRefList)
        
    def runVisit(self, cache, visitCcdId, rawRefList):
        '''Performs ISR, astrometry and, when needed, warp on all the exposures associated
        with a visit before combining them using snapCombine.'''
        selectList = self.selectExposures(visitCcdId, rawRefList)
        refWcs = None
        coaddExposure = None

        for selectRef in selectList:
            try:
                exposure = self.isr.runDataRef(selectRef).exposure
            except:
                self.log.warn("Unable to perform ISR for %s" % (selectRef.dataId,))
                continue
            try:
                exposure = self.astrometry.run(
                    dataRef=selectRef,
                    exposure=exposure)
                if exposure.hasWcs():
                    if refWcs == None:
                        refWcs=exposure.getWcs()
                else:
                    self.log.warn("No astrometry information for %s" % (selectRef.dataId,))
                    continue
            except:
                self.log.warn("Unable to perform astrometry on %s" % (selectRef.dataId,))
                continue

            warped = False
            if exposure.hasWcs():
                if refWcs != None and exposure.getWcs() != refWcs:
                    try:
                        exposure = self.warp.run(exposure, refWcs).direct
                        warped = True
                    except:
                        self.log.warn("Unable to warp %s" % (selectRef.dataId,))
                        continue
            
            if coaddExposure == None:
                coaddExposure = exposure
            else:
                if warped:
                    coaddExposure = self.snapCombine.run(coaddExposure, exposure).exposure

        #SelectRef is needed to generate a unique ID for detected sources;
        #Ensure that ID factory does not use run number, as that's different for each exposure
        #and we're using the last exposure to represent all exposures for that visit.
        
        charRes = self.charImage.run(
            dataRef=selectRef,
            exposure=coaddExposure,
            doUnpersist=False)

        calibRes = self.calibrate.run(
            dataRef=selectRef,
            exposure=charRes.exposure,
            background=charRes.background,
            doUnpersist=False,
            icSourceCat=charRes.sourceCat)
        
            
        #Write to disk:
        selectRef.put(calibRes.exposure, 'visitCoadd_calexp')
        
    def selectExposures(self, visitCcdId, rawRefList):
        return [rawRef
                for rawRef in rawRefList if
                ((rawRef.dataId['visit']<<4)+rawRef.dataId['ccd']) == visitCcdId]    
        
    def writeMetadata(self, dataRef):
        '''
        This is needed when passing a list to run, as metadate can't be written since a
        list doesn't have a dataId. See lsst/pipe/base/cmdLineTask.py.
        '''
        pass
