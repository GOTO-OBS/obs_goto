import os.path
from lsst.utils import getPackageDir
from lsst.meas.algorithms import SourceDetectionTask

for sub in ("mergeCoaddDetections",
            "measureCoaddSources",
            "mergeCoaddMeasurements",
            "forcedPhotCoadd"):
    path = os.path.join(getPackageDir("obs_goto"), "config", sub + ".py")
    if os.path.exists(path):
        getattr(config, sub).load(path)

config.doDetection=True
config.detectCoaddSources.doScaleVariance=True
config.detectCoaddSources.detection.doTempWideBackground=False

for i in [
        #'base_GaussianFlux', Needed for PSF in imageDifference.py
        'base_SdssShape',
        'base_ScaledApertureFlux',
        #'base_CircularApertureFlux', Needed for zeropoint
        'base_Blendedness',
        'base_NaiveCentroid',
        'base_LocalBackground',
        'base_Jacobian',
        'base_FPPosition',
        'base_Variance',
        'base_InputCount',
        #'base_SkyCoord', Needed for zeropoint
]:
    config.measureCoaddSources.measurement.plugins[i].doMeasure=False
    config.forcedPhotCoadd.measurement.plugins[i].doMeasure=False
    config.measureCoaddSources.measurement.undeblended[i].doMeasure=False
    config.forcedPhotCoadd.measurement.undeblended[i].doMeasure=False


