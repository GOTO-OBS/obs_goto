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

config.detection.thresholdValue = 14.0

#Cosmic rays and background estimation:
config.repair.doCosmicRay = False
config.detection.doTempLocalBackground=True
config.detection.tempLocalBackground.binSize = 32

#PSF determination:
config.psfIterations=1
config.measurePsf.reserveFraction = 0.2
config.measurePsf.starSelector["objectSize"].sourceFluxField = 'base_PsfFlux_flux'
try:
    import lsst.meas.extensions.psfex.psfexPsfDeterminer
    config.measurePsf.psfDeterminer["psfex"].spatialOrder = 2
    #config.measurePsf.psfDeterminer["psfex"].psfexBasis = 'PIXEL_AUTO'
    config.measurePsf.psfDeterminer["psfex"].samplingSize = 2.
    config.measurePsf.psfDeterminer["psfex"].kernelSize = 21
    config.measurePsf.psfDeterminer.name = "psfex"
except ImportError as e:
    print("WARNING: Unable to use psfex: %s" % e)
    config.measurePsf.psfDeterminer.name = "pca"

config.refObjLoader.defaultFilter ='m'

# Activate calibration of measurements: required for aperture corrections
config.load(os.path.join(configDir, "cmodel.py"))
config.measurement.load(os.path.join(configDir, "apertures.py"))
config.measurement.load(os.path.join(configDir, "kron.py"))
config.measurement.load(os.path.join(configDir, "convolvedFluxes.py"))

config.detection.includeThresholdMultiplier = 3.0

config.measurement.plugins['modelfit_CModel'].region.badMaskPlanes=['EDGE', 'SAT', 'BAD', 'NO_DATA']
config.measurement.undeblended['modelfit_CModel'].region.badMaskPlanes=['EDGE', 'SAT', 'BAD', 'NO_DATA']
config.measurement.undeblended['modelfit_CModel'].region.maxBadPixelFraction=None
config.measurement.plugins['modelfit_CModel'].region.maxBadPixelFraction=None

config.measureApCorr.starSelector['psfex'].maxbadflag=False
config.measureApCorr.starSelector['psfex'].badFlags=[]
config.measurePsf.psfDeterminer['psfex'].badMaskBits=[]
