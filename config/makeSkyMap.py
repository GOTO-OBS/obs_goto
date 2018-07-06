from lsst.obs.goto.printDict  import printDict

obj = printDict(config, path=['config'])

config.skyMap = "healpix"

# Configuration for HealpixSkyMap
config.skyMap["healpix"].log2NSide = 3
config.skyMap["healpix"].pixelScale = 1.2
config.skyMap["healpix"].patchInnerDimensions = (6000, 8000)
config.skyMap["healpix"].patchBorder = 100 # Pixels
config.skyMap["healpix"].tractOverlap = 1. # Degrees
config.skyMap["healpix"].projection = "TAN"

