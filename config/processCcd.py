#from lsst.obs.goto.gotoNullIsr import GotoNullIsrTask
from lsst.obs.goto.printDict  import printDict
import os.path
from lsst.utils import getPackageDir
configDir = os.path.join(getPackageDir("obs_goto"), "config")
#print('config/processCcd.py')

#Read post-ISR data:
#Note: this module can already "see" config variable:

#This recursively goes through an object and
#returns a list of all keys.: 
#obj = printDict(config, path=['config'])
#quit()

#config.charImage.doWriteExposure=False
#config.isr.doWrite=False
#config.isr.retarget(SwaspNullIsrTask)




config.isr.doBias=False
config.isr.doDark=False
config.isr.doFlat=False
config.charImage.repair.doCosmicRay = False
config.charImage.detection.thresholdValue = 5.0
config.calibrate.detection.thresholdValue = 5.0
#config.charImage.doDeblend = True
config.calibrate.doDeblend = True

#JRM uncommented this: 26/05/2017
config.charImage.measurePsf.starSelector["objectSize"].sourceFluxField = 'base_PsfFlux_flux'


config.charImage.measurement.load(os.path.join(configDir, "kron.py"))
config.calibrate.measurement.load(os.path.join(configDir, "kron.py"))

#config.charImage.load(os.path.join(configDir, "cmodel.py"))


config.calibrate.deblend.maskLimits["SAT"] =0

config.charImage.detection.doTempLocalBackground=True
config.calibrate.detection.doTempLocalBackground=True
config.charImage.detection.tempLocalBackground.binSize = 32
config.calibrate.detection.tempLocalBackground.binSize = 32

#config.charImage.astrometry.forceKnownWcs = True
#config.calibrate.astrometry.forceKnownWcs = True


config.calibrate.doAstrometry = True

config.calibrate.doPhotoCal = True

config.calibrate.photoCal.applyColorTerms = None
config.calibrate.photoCal.photoCatName = None
config.charImage.detection.includeThresholdMultiplier = 3.0

config.charImage.doMeasurePsf = True

#JRM commented this 26/05/2017
#config.charImage.measurePsf.psfDeterminer["pca"].reducedChi2ForPsfCandidates=10

config.charImage.doApCorr = True

config.calibrate.doApCorr = True

config.charImage.measurePsf.starSelector["objectSize"].fluxMin = 10000.
#config.charImage.measurePsf.starSelector["objectSize"].fluxMax = 10000

config.charImage.refObjLoader.defaultFilter ='m'

config.calibrate.astromRefObjLoader.defaultFilter ='m'
config.calibrate.astromRefObjLoader.filterMap ={'Clear':'m'}
config.calibrate.photoRefObjLoader.defaultFilter ='m'
config.calibrate.photoRefObjLoader.filterMap ={'Clear':'m'}
#config.calibrate.astrometry.matcher.minSnr = 3.

#Need to do this to remove overscan from
#calibration frame:
config.isr.doAssembleIsrExposures = True

#This could be messing up the variance, but is
#needed since we aren't calculating a variance
#plane for the calibration files.


#Sets the maximum match radius for astrometry matching:
config.calibrate.astrometry.matcher.maxMatchDistArcSec = 10.
config.calibrate.astrometry.matcher.maxOffsetPix = 20
config.calibrate.astrometry.matcher.maxRotationDeg = 1.
config.calibrate.astrometry.wcsFitter.maxScatterArcsec = 10.0
config.calibrate.photoCal.matcher.maxMatchDistArcSec = 10.0
#Also, need to set how far down in brightness we go down the
#reference catalogue. The default is 50, but this is too low
#for SWasp, as too many are saturated. 100 seems to be ok.
config.calibrate.astrometry.matcher.numBrightStars = 300
config.calibrate.photoCal.matcher.numBrightStars = 300
#Sets the default filter to use in the anet reference catalogue:
#config.calibrate.refObjLoader.filterMap['g']='v'
#config.calibrate.refObjLoader.load(os.path.join(getPackageDir("obs_swasp"), "config",
#                                                "filterMap.py")
