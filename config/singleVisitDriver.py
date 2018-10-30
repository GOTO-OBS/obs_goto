import os.path
from lsst.utils import getPackageDir

config.isr.load(os.path.join(getPackageDir("obs_goto"), "config", "isr.py"))
config.astrometry.load(os.path.join(getPackageDir("obs_goto"), "config", "astrometry.py"))

#Don't write charImage results:
config.charImage.doWrite = False

config.charImage.detection.thresholdValue = 5.0
config.charImage.detection.includeThresholdMultiplier = 10.0
config.charImage.detection.minPixels = 20

#Cosmic rays and background estimation:
config.charImage.repair.doCosmicRay = False
config.charImage.repair.cosmicray.nCrPixelMax=100000
config.charImage.repair.cosmicray.cond3_fac2 = 0.4
config.charImage.detection.doTempLocalBackground=True
config.charImage.detection.tempLocalBackground.binSize = 32

#PSF determination:
config.charImage.psfIterations=1
config.charImage.measurePsf.starSelector['objectSize'].widthMin=1.0
config.charImage.measurePsf.starSelector['objectSize'].widthMax=4.0
config.charImage.measurePsf.starSelector["objectSize"].fluxMin = 1000.
config.charImage.measurePsf.starSelector['objectSize'].widthStdAllowed=4.0
try:
    import lsst.meas.extensions.psfex.psfexPsfDeterminer
    #import lsst.meas.extensions.psfex.psfexStarSelector
    config.charImage.measurePsf.psfDeterminer["psfex"].spatialOrder = 2
    config.charImage.measurePsf.psfDeterminer["psfex"].psfexBasis = 'PIXEL_AUTO'
    config.charImage.measurePsf.psfDeterminer["psfex"].samplingSize = 0.7
    config.charImage.measurePsf.psfDeterminer["psfex"].kernelSize = 21
    config.charImage.measurePsf.psfDeterminer.name = "psfex"
except ImportError as e:
    print("WARNING: Unable to use psfex: %s" % e)
    config.charImage.measurePsf.psfDeterminer.name = "pca"
    
config.charImage.doApCorr = False

config.calibrate.load(os.path.join(getPackageDir("obs_goto"), "config", "calibrate.py"))

#Don't write to calexp, 
config.calibrate.doWrite = False

#Instead write to visitCalexp, visitSrc etc...
config.doWrite = True

config.forcedPhot.load(os.path.join(getPackageDir("obs_goto"), "config", "forcedPhotVisit.py"))
