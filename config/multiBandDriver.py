import os.path

from lsst.utils import getPackageDir
from lsst.obs.goto.printDict  import printDict

#obj = printDict(config, path=['config'])

#quit()

for sub in ("mergeCoaddDetections", "measureCoaddSources", "mergeCoaddMeasurements", "forcedPhotCoadd"):
    path = os.path.join(getPackageDir("obs_goto"), "config", sub + ".py")
    if os.path.exists(path):
        getattr(config, sub).load(path)
