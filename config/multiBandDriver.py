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
config.detectCoaddSources.detection.retarget(SourceDetectionTask)
config.detectCoaddSources.doScaleVariance=True
config.detectCoaddSources.detection.doTempWideBackground=False

config.deblendCoaddSources.singleBandDeblend.maxFootprintArea=10000
config.deblendCoaddSources.singleBandDeblend.propagateAllPeaks = False

for i in [#'base_PixelFlags',
          #'base_SdssCentroid',#Needed for positions
          'base_NaiveCentroid',
          'base_SdssShape',
          'base_GaussianFlux', #Needed for PSF in imageDifference.py
          'base_PsfFlux',
          #'base_CircularApertureFlux',
          #'base_SkyCoord',
          'base_Variance',
          'base_Blendedness',
          'base_LocalBackground',
          'base_ScaledApertureFlux',
          'base_InputCount',
]:
    config.measureCoaddSources.measurement.plugins[i].doMeasure=False
    config.forcedPhotCoadd.measurement.plugins[i].doMeasure=False
    config.measureCoaddSources.measurement.undeblended[i].doMeasure=False
    config.forcedPhotCoadd.measurement.undeblended[i].doMeasure=False


