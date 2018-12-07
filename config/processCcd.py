#from lsst.obs.goto.gotoNullIsr import GotoNullIsrTask
import os.path
from lsst.utils import getPackageDir
from lsst.meas.algorithms import ColorLimit
from lsst.meas.algorithms import LoadIndexedReferenceObjectsTask

configDir = os.path.join(getPackageDir("obs_goto"), "config")

#ISR:
config.isr.doWrite=False
config.isr.doAddDistortionModel = False
config.isr.doDefect = False
config.isr.doAssembleIsrExposures = False
config.isr.doBias=True
config.isr.doDark=True
config.isr.doFlat=True
config.isr.doSaturationInterpolation = False

#CharImage:
#Retarget the characterize image task to my own in gotoCharTask.
#Our own performs (almost) blind astrometry with aNet straight after ISR.
from lsst.obs.goto.gotoCharTask import GotoCharacterizeImageTask
config.charImage.retarget(GotoCharacterizeImageTask)
config.charImage.load(os.path.join(configDir, "characterizeImage.py"))

#Load Calibrate configurations
config.doCalibrate = True
config.calibrate.load(os.path.join(configDir, "calibrate.py"))
