import os.path
from lsst.utils import getPackageDir

#Use defaults from isr, charImage, calibrate and forcedPhot.
config.isr.load(os.path.join(getPackageDir("obs_goto"), "config", "isr.py"))
config.charImage.load(os.path.join(getPackageDir("obs_goto"), "config", "characterizeImage.py"))
config.calibrate.load(os.path.join(getPackageDir("obs_goto"), "config", "calibrate.py"))
config.forcedPhot.load(os.path.join(getPackageDir("obs_goto"), "config", "forcedPhotVisit.py"))

#Don't write to calexp, 
config.calibrate.doWrite = False

#Instead write to visitCalexp, visitSrc etc...
config.doWrite = True


