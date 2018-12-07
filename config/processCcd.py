import os.path
from lsst.utils import getPackageDir
from lsst.meas.algorithms import ColorLimit
from lsst.meas.algorithms import LoadIndexedReferenceObjectsTask

configDir = os.path.join(getPackageDir("obs_goto"), "config")

#ISR:
config.isr.load(os.path.join(configDir, "isr.py"))

#CharImage:
#Retarget the characterize image task to my own in gotoCharTask.
#Our own performs (almost) blind astrometry with aNet straight after ISR.
from lsst.obs.goto.gotoCharTask import GotoCharacterizeImageTask
config.charImage.retarget(GotoCharacterizeImageTask)
config.charImage.load(os.path.join(configDir, "characterizeImage.py"))

#Load Calibrate configurations
config.doCalibrate = True
config.calibrate.load(os.path.join(configDir, "calibrate.py"))
