from lsst.obs.goto.printDict  import printDict

obj = printDict(config, path=['config'])
print('***Lydia***: config/measureCoaddSources.py:' \
      'Setting doPropagateFlags to False. This could cause problems')
config.doPropagateFlags=False
config.match.refObjLoader.defaultFilter='m'
config.match.refObjLoader.filterMap ={'Clear':'m'}

#quit()
