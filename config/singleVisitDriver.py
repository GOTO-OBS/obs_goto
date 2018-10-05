import os.path
from lsst.utils import getPackageDir

config.isr.load(os.path.join(getPackageDir("obs_goto"), "config", "isr.py"))
config.astrometry.load(os.path.join(getPackageDir("obs_goto"), "config", "astrometry.py"))
