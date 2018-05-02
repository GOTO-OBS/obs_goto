from lsst.obs.goto.printDict  import printDict
import os.path
from lsst.utils import getPackageDir

#obj = printDict(config, path=['config'])
#quit()

print('***Lydia***: config/measureCoaddSources.py:' \
      'Setting doPropagateFlags to False. This could cause problems')
config.doPropagateFlags=False
config.match.refObjLoader.defaultFilter='m'
config.match.refObjLoader.filterMap ={'Clear':'m'}
config.load(os.path.join(getPackageDir("obs_goto"), "config", "cmodel.py"))
#quit()
config.doMatchSources=False
