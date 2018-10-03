from lsst.ctrl.pool.parallel import BatchPoolTask, BatchParallelTask
from lsst.ctrl.pool.pool import Pool, abortOnError, NODE
from lsst.pex.config import Config, ConfigurableField
import lsst.pipe.base as pipeBase
from lsst.pipe.base import ArgumentParser, ConfigDatasetType, TaskRunner
from lsst.pipe.tasks.processCcd import ProcessCcdTask

class RawDataIdContainer(pipeBase.DataIdContainer):
    def makeDataRefList(self, namespace):
        super(RawDataIdContainer, self).makeDataRefList(namespace)
        self.dataList = []
        for ref in self.refList:
            self.dataList.append(pipeBase.Struct(dataRef=ref))

class SingleVisitDriverConfig(Config):
    pass

class SingleVisitDriverTaskRunner(TaskRunner):
#    def __init__(self, TaskClass, parsedCmd, doReturnResults=False):
#        TaskRunner.__init__(self, TaskClass, parsedCmd, doReturnResults)
        
#    def makeTask(self, parsedCmd=None, args=None):
#        return self.TaskClass(config=self.config, log=self.log)

     @staticmethod
     def getTargetList(parsedCmd, **kwargs):
         """Task.run should receive a butler in the kwargs"""
         kwargs["butler"] = parsedCmd.butler
         return [(parsedCmd.id.refList, kwargs), ]

class SingleVisitDriverTask(BatchPoolTask):

    ConfigClass = SingleVisitDriverConfig
    _DefaultName = "singleVisitDriver"
    RunnerClass = SingleVisitDriverTaskRunner    

    def __init__(self, butler=None, *args, **kwargs):
        BatchPoolTask.__init__(self, *args, **kwargs)

    @classmethod
    def _makeArgumentParser(cls, **kwargs):
        parser = ArgumentParser(name=cls._DefaultName)
        parser.add_id_argument("--id", "raw",
                               level="sensor",
                               help="data ID, e.g. --id visit=12345 ccd=2",
                               ContainerClass=RawDataIdContainer)
        return parser

    def run(self, rawRefList, butler):
        #sensorRef and butler are passed from getTargetList
        uniqueVisits = set()
        for rawRef in rawRefList:
            uniqueVisits.add(rawRef.dataId['visit'])
        uniqueVisits = list(uniqueVisits)
        
