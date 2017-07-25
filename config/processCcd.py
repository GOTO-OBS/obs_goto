#from lsst.obs.goto.gotoNullIsr import GotoNullIsrTask
from lsst.obs.goto.printDict  import printDict
import os.path
from lsst.utils import getPackageDir
from lsst.meas.algorithms import LoadIndexedReferenceObjectsTask

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

config.charImage.detection.thresholdValue = 14.0
config.calibrate.detection.thresholdValue = 14.0

#Cosmic rays and background estimation:
config.charImage.repair.doCosmicRay = False
config.charImage.detection.doTempLocalBackground=True
config.calibrate.detection.doTempLocalBackground=True
config.charImage.detection.tempLocalBackground.binSize = 32
config.calibrate.detection.tempLocalBackground.binSize = 32

#PSF determination:
config.charImage.measurePsf.reserveFraction = 0.2
config.charImage.measurePsf.starSelector["objectSize"].sourceFluxField = 'base_PsfFlux_flux'
try:
    import lsst.meas.extensions.psfex.psfexPsfDeterminer
    config.charImage.measurePsf.psfDeterminer["psfex"].spatialOrder = 2
    #config.charImage.measurePsf.psfDeterminer["psfex"].psfexBasis = 'PIXEL_AUTO'
    config.charImage.measurePsf.psfDeterminer["psfex"].samplingSize = 2.
    config.charImage.measurePsf.psfDeterminer["psfex"].kernelSize = 21
    config.charImage.measurePsf.psfDeterminer.name = "psfex"
except ImportError as e:
    print("WARNING: Unable to use psfex: %s" % e)
    config.charImage.measurePsf.psfDeterminer.name = "pca"

config.charImage.refObjLoader.defaultFilter ='m'

#Astrometry:
config.calibrate.doAstrometry = True
config.calibrate.astrometry.matcher.sourceFluxType='Psf'
config.calibrate.astromRefObjLoader.defaultFilter ='m'
config.calibrate.astromRefObjLoader.filterMap ={'Clear':'m'}
config.calibrate.astrometry.matcher.numBrightStars = 500

#Sets the maximum match radius for astrometry matching:
config.calibrate.astrometry.matcher.maxMatchDistArcSec = 10.
config.calibrate.astrometry.matcher.maxOffsetPix = 20
config.calibrate.astrometry.matcher.maxRotationDeg = 1.
config.calibrate.astrometry.wcsFitter.maxScatterArcsec = 10.0

#Photometry:
config.calibrate.photoRefObjLoader.defaultFilter ='m'
config.calibrate.photoRefObjLoader.filterMap ={'Clear':'m'}
config.calibrate.photoCal.matcher.maxMatchDistArcSec = 10.0
config.calibrate.photoCal.matcher.numBrightStars = 500

# Demand astrometry and photoCal succeed
config.calibrate.requireAstrometry = True
config.calibrate.requirePhotoCal = True

# Activate calibration of measurements: required for aperture corrections
config.charImage.load(os.path.join(configDir, "cmodel.py"))
config.charImage.measurement.load(os.path.join(configDir, "apertures.py"))
config.charImage.measurement.load(os.path.join(configDir, "kron.py"))
config.charImage.measurement.load(os.path.join(configDir, "convolvedFluxes.py"))

config.calibrate.measurement.load(os.path.join(configDir, "apertures.py"))
config.calibrate.measurement.load(os.path.join(configDir, "kron.py"))

#Deblender:
config.calibrate.deblend.maskLimits["SAT"]=0

config.calibrate.photoCal.applyColorTerms = None
config.calibrate.photoCal.photoCatName = None
config.charImage.detection.includeThresholdMultiplier = 3.0

#Need to do this to remove overscan from
#calibration frame:
config.isr.doAssembleIsrExposures = True

#This could be messing up the variance, but is
#needed since we aren't calculating a variance
#plane for the calibration files.
config.isr.assembleCcd.setGain = False

#Also, need to set how far down in brightness we go down the
#reference catalogue. The default is 50, but this is too low
#for SWasp, as too many are saturated. 100 seems to be ok.
#Sets the default filter to use in the anet reference catalogue:
#config.calibrate.refObjLoader.filterMap['g']='v'
#config.calibrate.refObjLoader.load(os.path.join(getPackageDir("obs_swasp"), "config",
#                                                "filterMap.py")
