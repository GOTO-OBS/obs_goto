from lsst.pipe.tasks.characterizeImage import CharacterizeImageTask, CharacterizeImageConfig

class GotoCharacterizeImageConfig(CharacterizeImageConfig):
    print("GotoChar")

class GotoCharacterizeImageTask(CharacterizeImageTask):
    ConfigClass = GotoCharacterizeImageConfig

    def __init__(self, butler=None, refObjLoader=None, schema=None, **kwargs):
        super(GotoCharacterizeImageTask, self).__init__(**kwargs)

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
