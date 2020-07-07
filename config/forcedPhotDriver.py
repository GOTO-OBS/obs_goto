import os.path
from lsst.utils import getPackageDir

config.forcedPhot.load(os.path.join(getPackageDir("obs_goto"), "config", "forcedPhotCcd.py"))

