from lsst.obs.goto.printDict  import printDict
import os.path
#obj = printDict(config, path=['config'])
#quit()

from lsst.utils import getPackageDir

config.measurement.load(os.path.join(getPackageDir("obs_goto"), "config", "apertures.py"))
config.measurement.load(os.path.join(getPackageDir("obs_goto"), "config", "kron.py"))
config.load(os.path.join(getPackageDir("obs_goto"), "config", "cmodel.py"))

config.measurement.slots.instFlux = None
