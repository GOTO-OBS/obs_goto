import os
from lsst.utils import getPackageDir
from lsst.utils.introspection import get_full_type_name
from lsst.obs.base import Instrument, yamlCamera
from .gotoFilters import GOTO_FILTER_DEFINITIONS
from lsst.afw.cameraGeom import makeCameraFromPath, CameraConfig
# Comment-out the following line if you put .translators/necam.py in the
# astro_metadata_translator repository:
from .translators import GotoTranslator

class Goto(Instrument):

    # Filter definitions are needed when registering the filters.
    filterDefinitions = GOTO_FILTER_DEFINITIONS

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # Tell it where the config file are:
        packageDir = getPackageDir("obs_goto")
        self.configPaths = [os.path.join(packageDir, "config")]

    def getCamera(self):
        '''
        This grabs the camera information in the camera/u1_goto.yaml file.
        '''
        path = os.path.join(
            getPackageDir("obs_goto"),
            "camera",
            'u1_goto.yaml')
        camera = yamlCamera.makeCamera(path)
        return camera

    @classmethod
    def getName(cls):
        '''
        This must return the instrument name.
        '''
        return "Goto"

    def getRawFormatter(self, dataId):
        from .rawFormatter import NeCamRawFormatter
        return NeCamRawFormatter

    def makeDataIdTranslatorFactory(self):
        '''
        Needed to register instrument
        '''
        pass

    def register(self, registry, update=False):
        '''
        This populates the database with instrument and detector-specific information, and is implemented with:
        butler register-instrument DATA_REPO lsst.obs.necam.NeCam
        '''
        camera = self.getCamera()

        #Register the instrument:
        obsMax = 2**30 #GOTO can up to a billion images!
        with registry.transaction():
            registry.syncDimensionData(
                "instrument",
                {
                    "name": self.getName(),
                    "detector_max": 32,
                    "visit_max": obsMax,
                    "exposure_max": obsMax,
                    "class_name": get_full_type_name(self)
                }, update=update)

            #Register the detector(s):
            for detector in camera:
                registry.syncDimensionData(
                    "detector",
                    {
                        "instrument": self.getName(),
                        "id": detector.getId(),
                        "full_name": detector.getName(),
                        "name_in_raft": detector.getName(),
                        "raft": detector.getName(),
                        "purpose": str(detector.getType()).split(".")[-1],
                    },
                    update=update
                )

        #Registers the filter(s):
        self._registerFilters(registry)
