import os.path
from lsst.utils import getPackageDir

for sub in ("mergeCoaddDetections", "measureCoaddSources", "mergeCoaddMeasurements", "forcedPhotCoadd"):
    path = os.path.join(getPackageDir("obs_goto"), "config", sub + ".py")
    if os.path.exists(path):
        getattr(config, sub).load(path)

config.measureCoaddSources.deblend.maxFootprintSize = 0
config.measureCoaddSources.deblend.maxFootprintArea = 2000
