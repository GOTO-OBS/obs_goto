import os
from lsst.utils import getPackageDir
from lsst.utils.introspection import get_full_type_name
from lsst.obs.base import Instrument, yamlCamera
from .gotoFilters import GOTO_FILTER_DEFINITIONS
from lsst.afw.cameraGeom import makeCameraFromPath, CameraConfig
#from .rawFormatter import GotoRawFormatter, North1RawFormatter, North2RawFormatter

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
        # I'm calling a single GOTO rig a single "camera".
        # Each camera has eight UT's, each equiped with a single detector.
        # As far as the pipeline is concerned, a rig is a single camera
        # containing eight detectors.
        # This method must be overridden by the child class.
        return NotImplementedError()

    @classmethod
    def getName(cls):
        return NotImplementedError()

    def getRawFormatter(self, dataId):
        if dataId['instrument'] == 'North1':
            from .rawFormatter import North1RawFormatter, North2RawFormatter
            return North1RawFormatter
        elif dataId['instrument'] == 'North2':
            from .rawFormatter import North2RawFormatter
            return North2RawFormatter
        else:
            return NotImplementedError()

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
        obsMax = 2**30 #GOTO can take up to a billion images!
        with registry.transaction():
            registry.syncDimensionData(
                "instrument",
                {
                    "name": self.getName(),
                    "detector_max": 8,
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

class North1(Goto):

    def __init__(self, **kwargs):
        # This inherits the configPaths from GotoRig
        super().__init__(**kwargs)

    def getCamera(self):
        # I'm calling a single GOTO rig a single "camera".
        # Each camera has eight UT's, each equiped with a single detector.
        # As far as the pipeline is concerned,
        path = os.path.join(
            getPackageDir("obs_goto"),
            "camera",
            'n1_goto.yaml')
        camera = yamlCamera.makeCamera(path)
        return camera

    @classmethod
    def getName(cls):
        return "North1"

class North2(Goto):

    def __init__(self, **kwargs):
        # This inherits the configPaths from GotoRig
        super().__init__(**kwargs)

    def getCamera(self):
        # I'm calling a single GOTO rig a single "camera".
        # Each camera has eight UT's, each equiped with a single detector.
        # As far as the pipeline is concerned,
        path = os.path.join(
            getPackageDir("obs_goto"),
            "camera",
            'n2_goto.yaml')
        camera = yamlCamera.makeCamera(path)
        return camera

    @classmethod
    def getName(cls):
        return "North2"
