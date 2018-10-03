from lsst.ctrl.pool.parallel import BatchPoolTask, BatchParallelTask
from lsst.ctrl.pool.pool import Pool, abortOnError, NODE
from lsst.pex.config import Config, ConfigurableField
import lsst.pipe.base as pipeBase
from lsst.pipe.base import ArgumentParser, ConfigDatasetType, TaskRunner
from lsst.pipe.tasks.processCcd import ProcessCcdTask

class SingleVisitDriverConfig(Config):
    pass
    #processCcd = ConfigurableField(
    #            target=ProcessCcdTask, doc="CCD processing task")

class SingleVisitDriverTaskRunner(TaskRunner):
    pass
#    def __init__(self, TaskClass, parsedCmd, doReturnResults=False):
#        TaskRunner.__init__(self, TaskClass, parsedCmd, doReturnResults)
        
#    def makeTask(self, parsedCmd=None, args=None):
#        return self.TaskClass(config=self.config, log=self.log)

#    @staticmethod
#    def getTargetList(parsedCmd, **kwargs):
#        targetList = pipeBase.TaskRunner.getTargetList(parsedCmd,selectDataList=parsedCmd.id.refList,**kwargs)
#        return targetList

class SingleVisitDriverTask(BatchPoolTask):

    ConfigClass = SingleVisitDriverConfig
    _DefaultName = "singleVisitDriver"
    RunnerClass = SingleVisitDriverTaskRunner    

    def __init__(self, butler=None, *args, **kwargs):
        BatchParallelTask.__init__(self, *args, **kwargs)
        #self.makeSubtask('processCcd', butler=butler)
        
    @classmethod
    def _makeArgumentParser(cls, **kwargs):
        #kwargs.pop("doBatch", False)
        parser = ArgumentParser(name=cls._DefaultName)
        parser.add_id_argument("--id", "raw",
                               #ConfigDatasetType(
                               #    name="processCcd.isr.datasetType"),
                               level="sensor",
                               help="data ID, e.g. --id visit=12345 ccd=2")

        return parser

#    @classmethod
#    def batchWallTime(cls, time, parsedCmd, numCores):
#        numTargets = len(parsedCmd.id.refList)
#        return time*numTargets/float(numCores)
    
#    @abortOnError
#    def runDataRef(self, sensorRef):
#        print('BLAH')
#        import pdb
#        pdb.set_trace()
#        print(sensorRef)

    def run(self, sensorRef):
        import time
        time.sleep(5)
        print(sensorRef.dataId['visit'])

#Call this script with python3 -m singleVisitDriver.py"
#The -m is important!
#SingleVisitDriverTask.parseAndSubmit(['/local2/ph1jxm/GOTO/demoForcedPhot/DATA',
#                                      "--rerun", "outSVD",
#                                      "--id", "visit=54492..54494","ccd=4","filter=L",
#                                      "--cores", "1", "--clobber-config"])
