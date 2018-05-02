from lsst.obs.goto.printDict  import printDict

obj = printDict(config, path=['config'])
  
config.skyMap.patchInnerDimensions = [3000, 3000]
config.skyMap.patchBorder = 100
config.skyMap.projection="TAN"
config.skyMap.pixelScale=1.24



