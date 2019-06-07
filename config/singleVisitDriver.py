import os.path
from lsst.utils import getPackageDir

#Use defaults from isr, charImage, calibrate and forcedPhot.
config.isr.load(os.path.join(getPackageDir("obs_goto"), "config", "isr.py"))
config.charImage.load(os.path.join(getPackageDir("obs_goto"), "config", "characterizeImage.py"))
config.calibrate.load(os.path.join(getPackageDir("obs_goto"), "config", "calibrate.py"))
config.forcedPhot.load(os.path.join(getPackageDir("obs_goto"), "config", "forcedPhotVisit.py"))

config.calibrate.icSourceFieldsToCopy = ["calib_psfCandidate", "calib_psfUsed", "calib_psf_reserved"]

#Don't write to calexp, 
config.calibrate.doWrite = False

#Trying to stop memory leak:
config.calibrate.doDeblend = False
config.calibrate.doApCorr = False

#Currently not writing to visitCalexp, visitSrc etc...
config.doWrite = False


