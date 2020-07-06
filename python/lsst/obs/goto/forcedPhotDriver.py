from lsst.pex.config import Config, ConfigurableField
from lsst.pipe.base import ArgumentParser, ButlerInitializedTaskRunner, ConfigDatasetType
from lsst.ctrl.pool.parallel import BatchParallelTask, BatchTaskRunner
from .forcedPhotCalexp import ForcedPhotCalexpTask

class ForcedPhotDriverConfig(Config):
    forcedPhot = ConfigurableField(
        target=ForcedPhotCalexpTask,
        doc="Forced photometry task")

class ForcedPhotTaskRunner(BatchTaskRunner, ButlerInitializedTaskRunner):
    """Run batches, and initialize Task using a butler"""
    pass

class ForcedPhotDriverTask(BatchParallelTask):
    """Perform forced photometry on calexps in
    parallel.
    """
    ConfigClass = ForcedPhotDriverConfig
    _DefaultName = "forcedPhotDriver"
    RunnerClass = ForcedPhotTaskRunner

    def __init__(self, butler=None, *args, **kwargs):
        
        BatchParallelTask.__init__(self, *args, **kwargs)
        self.makeSubtask("forcedPhot", butler=butler)

    @classmethod
    def _makeArgumentParser(cls, *args, **kwargs):
        kwargs.pop("doBatch", False) #Not sure what this does or if it's necessary.
        parser = ArgumentParser(name=cls._DefaultName, *args, **kwargs)
        parser.add_id_argument("--id","calexp",
                               help="data ID, e.g. --id visit=12345 ccd=67")
        return parser


    def runDataRef(self, sensorRef):
        """Perform forced photometry on a single calexp
        """
        with self.logOperation("Performing forced photometry on  %s" % (sensorRef.dataId,)):
            self.forcedPhot.runDataRef(sensorRef)
