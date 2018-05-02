from lsst.obs.goto.printDict  import printDict

obj = printDict(config, path=['config'])

config.skyMap = "healpix"

# Configuration for HealpixSkyMap
config.skyMap["healpix"].log2NSide = 3
config.skyMap["healpix"].pixelScale = 1.4
config.skyMap["healpix"].patchBorder = 30 # Pixels
config.skyMap["healpix"].tractOverlap = 30./60. # Degrees
config.skyMap["healpix"].projection = "TAN"

