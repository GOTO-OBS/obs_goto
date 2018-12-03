from lsst.obs.goto.printDict  import printDict

obj = printDict(config, path=['config'])

config.skyMap = "healpix"

# Configuration for HealpixSkyMap
config.skyMap["healpix"].log2NSide = 2
config.skyMap["healpix"].pixelScale = 1.2
config.skyMap["healpix"].patchInnerDimensions = (4000, 4000)
config.skyMap["healpix"].patchBorder = 100 # Pixels
config.skyMap["healpix"].tractOverlap = 0.1 # Degrees
config.skyMap["healpix"].rotation = 45.
config.skyMap["healpix"].projection = "TAN"

