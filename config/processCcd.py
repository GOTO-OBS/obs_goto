#from lsst.obs.goto.gotoNullIsr import GotoNullIsrTask
from lsst.obs.goto.printDict  import printDict
import os.path
from lsst.utils import getPackageDir
#from lsst.meas.algorithms import LoadIndexedReferenceObjectsTask


configDir = os.path.join(getPackageDir("obs_goto"), "config")
#print('config/processCcd.py')

#Read post-ISR data:
#Note: this module can already "see" config variable:

#This recursively goes through an object and
#returns a list of all keys.: 
#obj = printDict(config, path=['config'])
#quit()

#config.charImage.doWriteExposure=False
config.isr.doWrite=True
#config.isr.retarget(SwaspNullIsrTask)

#Retarget the characterize image task to my own in gotoCharTask.
#Our own performs (almost) blind astrometry with aNet.
from lsst.obs.goto.gotoCharTask import GotoCharacterizeImageTask
config.charImage.retarget(GotoCharacterizeImageTask)

#config.isr.expectWcs = False
config.isr.doBias=True
config.isr.doDark=False
config.isr.doFlat=True
config.charImage.doEarlyAstrometry=True
config.charImage.earlyAstrometry.detection.includeThresholdMultiplier=30.0
config.charImage.earlyAstrometry.astromRefObjLoader.filterMap = {'L':'v'}

from lsst.meas.extensions.astrometryNet import ANetAstrometryTask
config.charImage.earlyAstrometry.astrometry.retarget(ANetAstrometryTask)
config.charImage.earlyAstrometry.astrometry.solver.useWcsRaDecCenter = False  # It's off for some reason dunno yet
config.charImage.earlyAstrometry.astrometry.solver.useWcsParity = False  # I doubt I guess right
config.charImage.earlyAstrometry.astrometry.solver.useWcsPixelScale = True  # DGM says it's 0.4, but....
config.charImage.earlyAstrometry.astrometry.solver.maxStars = 300            
config.charImage.earlyAstrometry.astrometry.solver.catalogMatchDist = 3.
config.charImage.earlyAstrometry.astrometry.solver.filterMap ={'L':'v'}

config.isr.doSaturationInterpolation = False
config.charImage.repair.doCosmicRay = False
config.charImage.detection.thresholdValue = 5.0
config.charImage.detection.includeThresholdMultiplier = 10.0
config.calibrate.detection.thresholdValue = 5.0
#config.charImage.doDeblend = True
config.calibrate.doDeblend = True
config.calibrate.deblend.maxFootprintSize = 0
config.calibrate.deblend.maxFootprintArea = 2000
config.calibrate.detection.isotropicGrow = True

config.isr.doAddDistortionModel = False

#If I use the default star selector, then I don't get any selected stars
try:
    import lsst.meas.extensions.psfex.psfexPsfDeterminer
    import lsst.meas.extensions.psfex.psfexStarSelector
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

config.charImage.measurement.load(os.path.join(configDir, "kron.py"))
config.calibrate.measurement.load(os.path.join(configDir, "kron.py"))

#config.charImage.load(os.path.join(configDir, "cmodel.py"))
config.calibrate.load(os.path.join(configDir, "cmodel.py"))

#config.calibrate.deblend.maskLimits["SAT"] =0

#config.charImage.detection.doTempLocalBackground=True
#config.calibrate.detection.doTempLocalBackground=True
#config.charImage.detection.tempLocalBackground.binSize = 128
#config.calibrate.detection.tempLocalBackground.binSize = 128


#config.charImage.astrometry.forceKnownWcs = True
config.calibrate.astrometry.forceKnownWcs = False


config.calibrate.doAstrometry = True

config.calibrate.doPhotoCal = True

config.calibrate.photoCal.applyColorTerms = None
config.calibrate.photoCal.photoCatName = None
config.charImage.doMeasurePsf = True

#config.charImage.detection.background.binSize = 512
#config.calibrate.detection.background.binSize = 512

#JRM commented this 26/05/2017
#config.charImage.measurePsf.psfDeterminer["pca"].reducedChi2ForPsfCandidates=10

config.charImage.doApCorr = True

config.calibrate.doApCorr = True

config.charImage.measurePsf.starSelector["objectSize"].fluxMin = 10000.
config.charImage.measurePsf.starSelector['objectSize'].widthStdAllowed=1.
#config.charImage.measurePsf.starSelector["objectSize"].fluxMax = 10000

#config.charImage.refObjLoader.defaultFilter ='m'
#config.calibrate.astromRefObjLoader.retarget(LoadIndexedReferenceObjectsTask)
#config.calibrate.astromRefObjLoader.ref_dataset_name = "UCAC4"

config.calibrate.astromRefObjLoader.defaultFilter ='m'
config.calibrate.astromRefObjLoader.filterMap ={'L':'v'}
config.calibrate.photoRefObjLoader.defaultFilter ='m'
config.calibrate.photoRefObjLoader.filterMap ={'L':'v'}
#config.calibrate.astrometry.matcher.minSnr = 3.

#Need to do this to remove overscan from
#calibration frame:
config.isr.doAssembleIsrExposures = False
config.isr.doDefect =False
#This could be messing up the variance, but is
#needed since we aren't calculating a variance
#plane for the calibration files.

#from lsst.meas.extensions.astrometryNet.anetAstrometry import ANetAstrometryTask
#config.calibrate.astrometry.retarget(ANetAstrometryTask)
#config.calibrate.astrometry.solver.sipOrder=3


#Sets the maximum match radius for astrometry matching:
config.calibrate.astrometry.matcher.maxMatchDistArcSec = 2.
config.calibrate.astrometry.matcher.maxOffsetPix = 50
config.calibrate.astromRefObjLoader.pixelMargin = 10
config.calibrate.astrometry.matcher.maxRotationDeg = 1.0
config.calibrate.astrometry.wcsFitter.order = 4


config.calibrate.astrometry.sourceSelection.flags.bad= ["base_PixelFlags_flag_edge"]
config.calibrate.astrometry.sourceSelection.doFlags = True

#config.calibrate.astrometry.referenceSelection.doFlags = True

config.calibrate.astrometry.wcsFitter.maxScatterArcsec = 10.0
#config.calibrate.photoCal.matcher.sourceSelector.active.sourceFluxType = 'Psf'
#config.calibrate.photoCal.matcher.maxMatchDistArcSec = 2.0
#config.calibrate.photoCal.matcher.maxOffsetPix = 90
#Also, need to set how far down in brightness we go down the
#reference catalogue. The default is 50, but this is too low
#for SWasp, as too many are saturated. 100 seems to be ok.
config.calibrate.astrometry.matcher.numBrightStars = 300
#config.calibrate.photoCal.matcher.numBrightStars = 300

#config.calibrate.photoCal.magLimit = 18
#config.calibrate.photoCal.doSelectUnresolved = False

