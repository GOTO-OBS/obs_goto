#from lsst.obs.goto.gotoNullIsr import GotoNullIsrTask
import os.path
from lsst.utils import getPackageDir
from lsst.meas.algorithms import LoadIndexedReferenceObjectsTask

configDir = os.path.join(getPackageDir("obs_goto"), "config")
#Retarget the characterize image task to my own in gotoCharTask.
#Our own performs (almost) blind astrometry with aNet straight after ISR.
#from lsst.obs.goto.gotoCharTask import GotoCharacterizeImageTask
#config.retarget(GotoCharacterizeImageTask)

config.doWriteExposure=True
config.doEarlyAstrometry=True
config.earlyAstrometry.detection.includeThresholdMultiplier = 10.0
config.earlyAstrometry.astromRefObjLoader.filterMap = {'L':'v'}
config.earlyAstrometry.detection.minPixels = 5

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
        'base_SkyCoord']:
    config.earlyAstrometry.measurement.plugins[i].doMeasure=False

#But a few more needed for measurePsf:
#config.charImage.measurement.plugins[i].doMeasure=False

from lsst.meas.extensions.astrometryNet import ANetAstrometryTask
config.earlyAstrometry.astrometry.retarget(ANetAstrometryTask)
config.earlyAstrometry.astrometry.solver.useWcsRaDecCenter = True
config.earlyAstrometry.astrometry.solver.useWcsParity = True
config.earlyAstrometry.astrometry.solver.useWcsPixelScale = True
config.earlyAstrometry.astrometry.solver.raDecSearchRadius = 5.
config.earlyAstrometry.astrometry.solver.maxStars = 1000
config.earlyAstrometry.astrometry.solver.catalogMatchDist = 30.
config.earlyAstrometry.astrometry.solver.pixelScaleUncertainty= 1.2
config.earlyAstrometry.astrometry.solver.filterMap = {'L':'v'}
config.earlyAstrometry.astrometry.solver.pixelMargin = 1000
config.earlyAstrometry.astrometry.solver.sipOrder = 3
config.earlyAstrometry.astrometry.solver.calculateSip = True
config.earlyAstrometry.astrometry.solver.maxIter = 20
config.earlyAstrometry.astrometry.solver.matchDistanceSigma = 2.0
config.earlyAstrometry.astrometry.solver.cleaningParameter = 5.0

config.earlyAstrometry.astrometry.rejectThresh = 3.0

config.detection.thresholdValue = 5.0
config.detection.includeThresholdMultiplier = 10.0
config.detection.minPixels = 20

#Cosmic rays and background estimation:
config.repair.doCosmicRay = True
config.repair.cosmicray.nCrPixelMax=100000
config.repair.cosmicray.cond3_fac2 = 0.4
config.detection.doTempLocalBackground=True
config.detection.tempLocalBackground.binSize = 32

#PSF determination:
config.psfIterations=1
#config.measurePsf.reserveFraction = 0.2
#config.measurePsf.starSelector["objectSize"].sourceFluxField = 'base_PsfFlux_flux'

config.measurePsf.starSelector['objectSize'].widthMin=1.0
config.measurePsf.starSelector['objectSize'].widthMax=4.0
#config.measurePsf.starSelector['secondMoment'].clumpNSigma=3.0
config.measurePsf.starSelector["objectSize"].fluxMin = 1000.
config.measurePsf.starSelector['objectSize'].widthStdAllowed=4.0
try:
    import lsst.meas.extensions.psfex.psfexPsfDeterminer
    #import lsst.meas.extensions.psfex.psfexStarSelector
    config.measurePsf.psfDeterminer["psfex"].spatialOrder = 2
    config.measurePsf.psfDeterminer["psfex"].psfexBasis = 'PIXEL_AUTO'
    config.measurePsf.psfDeterminer["psfex"].samplingSize = 0.7
    config.measurePsf.psfDeterminer["psfex"].kernelSize = 21
    config.measurePsf.psfDeterminer.name = "psfex"
except ImportError as e:
    print("WARNING: Unable to use psfex: %s" % e)
    config.measurePsf.psfDeterminer.name = "pca"

config.doApCorr = False

#config.refObjLoader.defaultFilter ='m'

# Activate calibration of measurements: required for aperture corrections
#config.load(os.path.join(configDir, "cmodel.py"))
#config.measurement.load(os.path.join(configDir, "apertures.py"))
#config.measurement.load(os.path.join(configDir, "kron.py"))
#config.measurement.load(os.path.join(configDir, "convolvedFluxes.py"))

#config.detection.includeThresholdMultiplier = 3.0

#config.measurement.plugins['modelfit_CModel'].region.badMaskPlanes=['EDGE', 'SAT', 'BAD', 'NO_DATA']
#config.measurement.undeblended['modelfit_CModel'].region.badMaskPlanes=['EDGE', 'SAT', 'BAD', 'NO_DATA']
#config.measurement.undeblended['modelfit_CModel'].region.maxBadPixelFraction=None
#config.measurement.plugins['modelfit_CModel'].region.maxBadPixelFraction=None



#config.measureApCorr.starSelector['psfex'].maxbadflag=False
#config.measureApCorr.starSelector['psfex'].badFlags=[]
#config.measurePsf.psfDeterminer['psfex'].badMaskBits=[]
