from lsst.obs.goto.printDict  import printDict
import os.path
from lsst.utils import getPackageDir

#obj = printDict(config, path=['config'])
#quit()

print('***Lydia***: config/measureCoaddSources.py:' \
      'Setting doPropagateFlags to False. This could cause problems')
config.doPropagateFlags=False
for source, target in [('B', 'b'), ('G', 'v'), ('R', 'm'), ('L', 'v')]:
    config.match.refObjLoader.filterMap[source]=target
#config.load(os.path.join(getPackageDir("obs_goto"), "config", "cmodel.py"))
#quit()
config.doMatchSources=False
