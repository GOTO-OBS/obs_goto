import os.path
from lsst.utils import getPackageDir
from lsst.meas.algorithms import SourceDetectionTask
from lsst.obs.goto.propagateGotoVisitFlags import PropagateGotoVisitFlagsTask 

for sub in ("mergeCoaddDetections", "measureCoaddSources", "mergeCoaddMeasurements", "forcedPhotCoadd"):
    path = os.path.join(getPackageDir("obs_goto"), "config", sub + ".py")
    if os.path.exists(path):
        getattr(config, sub).load(path)
config.doDetection=True
config.detectCoaddSources.detection.retarget(SourceDetectionTask)
config.detectCoaddSources.doScaleVariance=False
config.detectCoaddSources.detection.thresholdValue = 3.0

config.measureCoaddSources.deblend.maxFootprintArea = 2000
config.measureCoaddSources.deblend.propagateAllPeaks = False

config.measureCoaddSources.propagateFlags.retarget(PropagateGotoVisitFlagsTask)


for i in [
        #'base_GaussianFlux', Needed for PSF in imageDifference.py
        #'base_SdssShape',
        'base_ScaledApertureFlux',
        #'base_CircularApertureFlux', Needed for zeropoint
        'base_Blendedness',
        'base_LocalBackground',
        #'base_Jacobian',
        #'base_FPPosition',
        'base_Variance',
        'base_InputCount',
        #'base_SkyCoord', Needed for zeropoint
]:
    config.measureCoaddSources.measurement.plugins[i].doMeasure=False
    config.forcedPhotCoadd.measurement.plugins[i].doMeasure=False
    config.measureCoaddSources.measurement.undeblended[i].doMeasure=False
    config.forcedPhotCoadd.measurement.undeblended[i].doMeasure=False


