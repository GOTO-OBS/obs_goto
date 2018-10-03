from lsst.ctrl.pool.parallel import BatchPoolTask, BatchParallelTask
from lsst.ctrl.pool.pool import Pool, abortOnError, NODE
from lsst.pex.config import Config, ConfigurableField
import lsst.pipe.base as pipeBase
from lsst.pipe.base import ArgumentParser, ConfigDatasetType, TaskRunner
from lsst.pipe.tasks.processCcd import ProcessCcdTask

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
         #kwargs["butler"] = parsedCmd.butler
         #for ref in parsedCmd.id.refList:
         #    print(ref.dataId)
         #return [(parsedCmd.id.refList, kwargs), ]
         return TaskRunner.getTargetList(parsedCmd, butler=parsedCmd.butler, selectDataList=parsedCmd.id.refList, **kwargs)

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
                               help="data ID, e.g. --id visit=12345 ccd=2")
        #I think I have to make my own dataIdContainer to create a dataList
        return parser

    def run(self, sensorRef, butler, selectDataList=[]):
        #sensorRef and butler are passed from pipeBase.TaskRunner.getTargetList
        print(selectDataList)
        print('run')
