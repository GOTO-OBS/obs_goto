import os.path
from lsst.utils import getPackageDir
config.detection.includeThresholdMultiplier = 10.0

for source, target in [('B', 'b'), ('G', 'v'), ('R', 'm'), ('L', 'v')]:
    config.astromRefObjLoader.filterMap[source]=target

config.detection.minPixels = 5

from lsst.meas.extensions.astrometryNet import ANetAstrometryTask
config.astrometry.retarget(ANetAstrometryTask)

config.astrometry.solver.useWcsRaDecCenter = True
config.astrometry.solver.useWcsParity = True
config.astrometry.solver.useWcsPixelScale = True
config.astrometry.solver.raDecSearchRadius = 5.
config.astrometry.solver.maxStars = 1000
config.astrometry.solver.catalogMatchDist = 30.
config.astrometry.solver.pixelScaleUncertainty= 1.2
#config.earlyAstrometry.astrometry.solver.filterMap = {'L':'v'}
for source, target in [('B', 'b'), ('G', 'v'), ('R', 'm'), ('L', 'v')]:
    config.astrometry.solver.filterMap[source]=target
config.astrometry.solver.pixelMargin = 1000
config.astrometry.solver.sipOrder = 3
config.astrometry.solver.calculateSip = True
config.astrometry.solver.maxIter = 20
config.astrometry.solver.matchDistanceSigma = 2.0
config.astrometry.solver.cleaningParameter = 5.0
    
config.astrometry.rejectThresh = 3.0
