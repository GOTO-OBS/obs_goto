from lsst.pipe.tasks.characterizeImage import CharacterizeImageTask, CharacterizeImageConfig
import lsst.pex.config as pexConfig
from .astrometry import AstrometryTask


class GotoCharacterizeImageConfig(CharacterizeImageConfig):
    doEarlyAstrometry = pexConfig.Field(
        dtype=bool,
        default=False,
        doc="Perform astrometry on raw frame (only needed if raw frame does not come with a WCS solution",
    )

    earlyAstrometry = pexConfig.ConfigurableField(
        target = AstrometryTask,
        doc="""Task to obtain an initial WCS should your raw data not come with a WCS solution.""",
    )
            
class GotoCharacterizeImageTask(CharacterizeImageTask):
    ConfigClass = GotoCharacterizeImageConfig

    def __init__(self, butler=None, astromRefObjLoader=None, schema=None, **kwargs):
        super(GotoCharacterizeImageTask, self).__init__(**kwargs)
        self.makeSubtask("earlyAstrometry", butler=butler, astromRefObjLoader=astromRefObjLoader)
        
    def run(self, dataRef, exposure=None, background=None, doUnpersist=True):

        self.log.info("gotoCharTask Processing %s" % (dataRef.dataId))

        if doUnpersist:
            if exposure is not None or background is not None:
                raise RuntimeError("doUnpersist true; exposure and background must be None")
            exposure = dataRef.get("postISRCCD", immediate=True)
        elif exposure is None:
            raise RuntimeError("doUnpersist false; exposure must be provided")
        
        exposure = dataRef.get("postISRCCD", immediate=True)
        exposureIdInfo = dataRef.get("expIdInfo")

        if self.config.doEarlyAstrometry:
            exposure = self.earlyAstrometry.run(
                dataRef=dataRef,
                exposure=exposure,
            )

        charRes = self.characterize(
                        exposure=exposure,
                        exposureIdInfo=exposureIdInfo,
                        background=background)

        if self.config.doWrite:
            dataRef.put(charRes.sourceCat, "icSrc")
            if self.config.doWriteExposure:
                dataRef.put(charRes.exposure, "icExp")
                dataRef.put(charRes.background, "icExpBackground")

        return charRes
