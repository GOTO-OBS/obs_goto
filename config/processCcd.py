#from lsst.obs.goto.gotoNullIsr import GotoNullIsrTask
import os.path
from lsst.utils import getPackageDir
from lsst.meas.algorithms import ColorLimit
from lsst.meas.algorithms import LoadIndexedReferenceObjectsTask

configDir = os.path.join(getPackageDir("obs_goto"), "config")

#ISR:
config.isr.doWrite=True
config.isr.doAddDistortionModel = False
config.isr.doDefect = False
config.isr.doAssembleIsrExposures = False
config.isr.doBias=True
config.isr.doDark=True
config.isr.doFlat=True
config.isr.doSaturationInterpolation = False

#CharImage:
#Retarget the characterize image task to my own in gotoCharTask.
#Our own performs (almost) blind astrometry with aNet straight after ISR.
from lsst.obs.goto.gotoCharTask import GotoCharacterizeImageTask
config.charImage.retarget(GotoCharacterizeImageTask)
config.charImage.load(os.path.join(getPackageDir("obs_goto"), "config", "characterizeImage.py"))

#Calibrate configs:
config.doCalibrate = True # Do we need to calibrate for difference imaging?

for i in [
        #'base_GaussianFlux', Needed for PSF in imageDifference.py
        #'base_SdssShape',
        'base_ScaledApertureFlux',
        #'base_CircularApertureFlux', Needed for zeropoint
        'base_Blendedness',
        #'base_LocalBackground',
        'base_Jacobian',
        'base_FPPosition',
        #'base_Variance',
        'base_InputCount',
        #'base_SkyCoord', Needed for zeropoint
        ]:
    config.calibrate.measurement.plugins[i].doMeasure=False
        
config.calibrate.detection.thresholdValue = 20.0
config.calibrate.doDeblend = True
config.calibrate.deblend.maxFootprintSize = 0
config.calibrate.deblend.maxFootprintArea = 2000
config.calibrate.detection.isotropicGrow = True

#config.calibrate.measurement.load(os.path.join(configDir, "kron.py"))
#config.calibrate.load(os.path.join(configDir, "cmodel.py"))

#config.calibrate.deblend.maskLimits["SAT"] =0
#config.calibrate.detection.doTempLocalBackground=True
#config.calibrate.detection.tempLocalBackground.binSize = 128

config.calibrate.astrometry.forceKnownWcs = True
config.calibrate.doAstrometry = False
config.calibrate.doPhotoCal = True


colors = config.calibrate.photoCal.match.referenceSelection.colorLimits
config.calibrate.photoCal.colorterms.load(os.path.join(configDir, 'colorterms.py'))
config.calibrate.photoCal.applyColorTerms = False

config.calibrate.photoCal.match.referenceSelection.doMagLimit = True
config.calibrate.photoCal.match.referenceSelection.magLimit.fluxField = "i_flux"
colors["r-i"] = ColorLimit(primary="r_flux", secondary="i_flux", maximum=0.5)
colors["g-r"] = ColorLimit(primary="g_flux", secondary="r_flux", minimum=0.0)
config.calibrate.photoCal.match.referenceSelection.magLimit.maximum = 19.0
config.calibrate.photoCal.match.referenceSelection.magLimit.minimum = 13.0



config.calibrate.photoRefObjLoader.retarget(LoadIndexedReferenceObjectsTask)
config.calibrate.photoRefObjLoader.ref_dataset_name = "ps1_pv3_3pi_20170110"

for source, target in [('B', 'g'), ('G', 'g'), ('R', 'r'), ('L', 'g')]:
    config.calibrate.photoRefObjLoader.filterMap[source]=target

config.calibrate.photoCal.photoCatName = "ps1_pv3_3pi_20170110"
config.calibrate.doApCorr = False



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

