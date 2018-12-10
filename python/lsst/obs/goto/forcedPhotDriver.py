from lsst.pex.config import Config, ConfigurableField
from lsst.pipe.base import ButlerInitializedTaskRunner
from lsst.ctrl.pool.parallel import BatchParallelTask, BatchTaskRunner

class ForcedPhotDriverConfig(Config):
    forcedPhot = ConfigurableField(
        target=ForcedPhotCcdTask,
        doc="Forced photometry task")

class ForcedPhotTaskRunner(BatchTaskRunner, ButlerInitializedTaskRunner):

class ForcedPhotTask(BatchParallelTask):
    """Perform forced photometry on calexps in
    parallel.
    """
    ConfigClass = ForcedPhotDriverConfig
    _DefaultName = "forcedPhotDriver"
    RunnerClass = ForcedPhotTaskRunner

    def __init__(self, butler=None, psfRefObjLoader=None, astromRefObjLoader=None, photoRefObjLoader=None,
                 *args, **kwargs):
        
