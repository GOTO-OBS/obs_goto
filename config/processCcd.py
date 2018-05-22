#from lsst.obs.goto.gotoNullIsr import GotoNullIsrTask
import os.path
from lsst.utils import getPackageDir
#from lsst.meas.algorithms import LoadIndexedReferenceObjectsTask

configDir = os.path.join(getPackageDir("obs_goto"), "config")

#Read post-ISR data:
config.isr.doWrite=True

#Retarget the characterize image task to my own in gotoCharTask.
#Our own performs (almost) blind astrometry with aNet straight after ISR.
from lsst.obs.goto.gotoCharTask import GotoCharacterizeImageTask
config.charImage.retarget(GotoCharacterizeImageTask)

config.isr.doAddDistortionModel = False
config.isr.doDefect = False
config.isr.doAssembleIsrExposures = False
config.isr.doBias=True
config.isr.doDark=True
config.isr.doFlat=True
config.isr.doSaturationInterpolation = False

#CharImage:
config.charImage.doEarlyAstrometry=True
config.charImage.earlyAstrometry.detection.includeThresholdMultiplier=10.0
config.charImage.earlyAstrometry.astromRefObjLoader.filterMap = {'L':'v'}
config.charImage.earlyAstrometry.detection.minPixels = 100

#Don't make lots of measurements if we can avoid it:
#Dew needed for earlyAstrometry:
for i in [
#        'base_GaussianFlux',
#        'base_SdssShape', #base_SdssShape is needed for PSF determination.
        'base_ScaledApertureFlux',
        'base_CircularApertureFlux',
        'base_Blendedness',
        'base_LocalBackground',
        'base_Jacobian',
        'base_FPPosition',
        'base_Variance',
        'base_InputCount',
        'base_SkyCoord'
]:
    config.charImage.earlyAstrometry.measurement.plugins[i].doMeasure=False

#But a few more needed for measurePsf:
#config.charImage.measurement.plugins[i].doMeasure=False

#MatchOptimisticB (this does not work):
#config.charImage.earlyAstrometry.astromRefObjLoader.pixelMargin = 5000
#config.charImage.earlyAstrometry.astrometry.matcher.numBrightStars = 150
#config.charImage.earlyAstrometry.astrometry.matcher.maxOffsetPix = 2000
#config.charImage.earlyAstrometry.astrometry.matcher.maxMatchDistArcSec = 10.

#Astrometry.net (this now works very well):
from lsst.meas.extensions.astrometryNet import ANetAstrometryTask
config.charImage.earlyAstrometry.astrometry.retarget(ANetAstrometryTask)
config.charImage.earlyAstrometry.astrometry.solver.useWcsRaDecCenter = True
config.charImage.earlyAstrometry.astrometry.solver.useWcsParity = True
config.charImage.earlyAstrometry.astrometry.solver.useWcsPixelScale = True
config.charImage.earlyAstrometry.astrometry.solver.raDecSearchRadius = 5.
config.charImage.earlyAstrometry.astrometry.solver.maxStars = 500            
config.charImage.earlyAstrometry.astrometry.solver.catalogMatchDist = 10.
config.charImage.earlyAstrometry.astrometry.solver.pixelScaleUncertainty= 1.02
config.charImage.earlyAstrometry.astrometry.solver.filterMap = {'L':'v'}
config.charImage.earlyAstrometry.astrometry.solver.pixelMargin = 1000
config.charImage.earlyAstrometry.astrometry.solver.sipOrder = 4
config.charImage.earlyAstrometry.astrometry.solver.calculateSip = True

config.charImage.repair.doCosmicRay = False
config.charImage.detection.thresholdValue = 5.0
config.charImage.detection.includeThresholdMultiplier = 10.0

#If I use the default star selector, then I don't get any selected stars
config.charImage.doMeasurePsf = True
try:
    import lsst.meas.extensions.psfex.psfexPsfDeterminer
#    import lsst.meas.extensions.psfex.psfexStarSelector
    config.charImage.measurePsf.psfDeterminer["psfex"].spatialOrder = 3
    config.charImage.measurePsf.psfDeterminer["psfex"].psfexBasis = 'PIXEL_AUTO'
    config.charImage.measurePsf.psfDeterminer["psfex"].samplingSize = 0.0
    config.charImage.measurePsf.psfDeterminer["psfex"].kernelSize = 35
    config.charImage.measurePsf.psfDeterminer["psfex"].recentroid=True
    #config.charImage.measurePsf.psfDeterminer["psfex"].tolerance=1
    config.charImage.measurePsf.psfDeterminer.name = "psfex"
except ImportError as e:
    print("WARNING: Unable to use psfex: %s" % e)
    config.charImage.measurePsf.psfDeterminer.name = "pca"

#JRM commented this: 03/04/2017
#config.charImage.measurePsf.starSelector["objectSize"].sourceFluxField = 'base_PsfFlux_flux'
#config.charImage.doMeasurePsf = False

config.charImage.doApCorr = False

config.charImage.measurePsf.starSelector["objectSize"].fluxMin = 10000.
config.charImage.measurePsf.starSelector['objectSize'].widthStdAllowed=1.
#config.charImage.measurePsf.starSelector["objectSize"].fluxMax = 10000

#Calibrate configs:
config.doCalibrate = False # Do we need to calibrate for difference imaging?
config.calibrate.detection.thresholdValue = 5.0
config.calibrate.doDeblend = True
config.calibrate.deblend.maxFootprintSize = 0
config.calibrate.deblend.maxFootprintArea = 2000
config.calibrate.detection.isotropicGrow = True

config.calibrate.measurement.load(os.path.join(configDir, "kron.py"))
config.calibrate.load(os.path.join(configDir, "cmodel.py"))

#config.calibrate.deblend.maskLimits["SAT"] =0
#config.calibrate.detection.doTempLocalBackground=True
#config.calibrate.detection.tempLocalBackground.binSize = 128

config.calibrate.astrometry.forceKnownWcs = True
config.calibrate.doAstrometry = False
config.calibrate.doPhotoCal = True

config.calibrate.photoCal.applyColorTerms = None
config.calibrate.photoCal.photoCatName = None

config.calibrate.doApCorr = True

#config.calibrate.astromRefObjLoader.retarget(LoadIndexedReferenceObjectsTask)
#config.calibrate.astromRefObjLoader.ref_dataset_name = "UCAC4"

#config.calibrate.astromRefObjLoader.defaultFilter ='m'
#config.calibrate.astromRefObjLoader.filterMap ={'L':'v'}
#config.calibrate.photoRefObjLoader.defaultFilter ='m'
config.calibrate.photoRefObjLoader.filterMap ={'L':'v'}
#config.calibrate.astrometry.matcher.minSnr = 3.

#Need to do this to remove overscan from
#calibration frame:

#This could be messing up the variance, but is
#needed since we aren't calculating a variance
#plane for the calibration files.

#from lsst.meas.extensions.astrometryNet.anetAstrometry import ANetAstrometryTask
#config.calibrate.astrometry.retarget(ANetAstrometryTask)
#config.calibrate.astrometry.solver.sipOrder=3


#Sets the maximum match radius for astrometry matching:
#config.calibrate.astrometry.matcher.maxMatchDistArcSec = 2.
#config.calibrate.astrometry.matcher.maxOffsetPix = 50
#config.calibrate.astromRefObjLoader.pixelMargin = 10
#config.calibrate.astrometry.matcher.maxRotationDeg = 1.0
#config.calibrate.astrometry.wcsFitter.order = 4


#config.calibrate.astrometry.sourceSelection.flags.bad= ["base_PixelFlags_flag_edge"]
#config.calibrate.astrometry.sourceSelection.doFlags = True

#config.calibrate.astrometry.referenceSelection.doFlags = True

#config.calibrate.astrometry.wcsFitter.maxScatterArcsec = 10.0
#config.calibrate.photoCal.matcher.sourceSelector.active.sourceFluxType = 'Psf'
#config.calibrate.photoCal.matcher.maxMatchDistArcSec = 2.0
#config.calibrate.photoCal.matcher.maxOffsetPix = 90
#Also, need to set how far down in brightness we go down the
#reference catalogue. The default is 50, but this is too low
#for SWasp, as too many are saturated. 100 seems to be ok.
#config.calibrate.astrometry.matcher.numBrightStars = 300
#config.calibrate.photoCal.matcher.numBrightStars = 300

#config.calibrate.photoCal.magLimit = 18
#config.calibrate.photoCal.doSelectUnresolved = False

