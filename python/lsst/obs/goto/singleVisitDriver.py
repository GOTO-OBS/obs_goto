from lsst.ctrl.pool.parallel import BatchPoolTask, BatchParallelTask
from lsst.ctrl.pool.pool import Pool, abortOnError, NODE
from lsst.pex.config import Config, ConfigurableField
import lsst.pipe.base as pipeBase
from lsst.pipe.base import ArgumentParser, ConfigDatasetType, TaskRunner
from lsst.pipe.tasks.processCcd import ProcessCcdTask
from lsst.ip.isr import IsrTask

class RawDataIdContainer(pipeBase.DataIdContainer):
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

    astrometry = pexConfig.ConfigurableField(
        target = AstrometryTask,
        doc="""Task to obtain an initial WCS should your raw data not come with a WCS solution.""")
    
class SingleVisitDriverTaskRunner(TaskRunner):

    def __init__(self, TaskClass, parsedCmd, doReturnResults=True):
        TaskRunner.__init__(self, TaskClass, parsedCmd, doReturnResults)
        
    def makeTask(self, parsedCmd=None, args=None):
        return self.TaskClass(config=self.config, log=self.log)
    
    @staticmethod
    def getTargetList(parsedCmd, **kwargs):
        """Passes the data reference list and butler to run()."""
        kwargs["butler"] = parsedCmd.butler
        return [(parsedCmd.id.refList, kwargs), ]

class SingleVisitDriverTask(BatchPoolTask):

    ConfigClass = SingleVisitDriverConfig
    _DefaultName = "singleVisitDriver"
    RunnerClass = SingleVisitDriverTaskRunner    

    def __init__(self, *args, **kwargs):
        BatchPoolTask.__init__(self, *args, **kwargs)
        self.makeSubtask("isr")
        self.makeSubtask("astrometry")
        
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
        visitIdList = list(set([rawRef.dataId['visit']
                                for rawRef in rawRefList]))

        #Map visits out to separate (sets of) nodes:
        pool.map(self.runVisit, visitIdList, rawRefList)
        
#        return None

    def runVisit(self, cache, visitId, rawRefList):
        '''Performs ISR, astrometry and, when needed, warp on all the exposures associated
        with a visit before combining them using snapCombine.'''
        
        selectList = self.selectExposures(visitId, rawRefList)
        refWcs = None
        refExposure = None
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
                if exposure.hasWcs:
                    if refWcs == None:
                        refWcs=exposure.wcs
                else:
                    self.log.warn("No astrometry information for %s" % (selectRef.dataId,))
                    continue
            except:
                self.log.warn("Unable to perform astrometry on %s" % (selectRef.dataId,))
                continue
            
            warped = False
            if exposure.hasWcs:
                if refWcs != None and exposure.wcs != refWcs:
                    try:
                        exposure = self.warp.run(exposure, refWcs)
                        warped = True
                    except:
                        self.log.warn("Unable to warp %s" % (selectRef.dataId,))
                        continue

            if refExposure == None:
                refExposure = exposure
            else:
                if warped:
                    refExposure = self.snapCombine(refExposure, exposure)
                
                    
    def selectExposures(self, visitId, rawRefList):
        return [rawRef for rawRef in rawRefList if rawRef.dataId['visit'] == visitId]

        
    def writeMetadata(self, dataRef):
        '''
        This is needed when passing a list to run, as metadate can't be written since a
        list doesn't have a dataId. See lsst/pipe/base/cmdLineTask.py.
        '''
        pass
