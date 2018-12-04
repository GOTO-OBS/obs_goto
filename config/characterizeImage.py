from lsst.meas.algorithms import LoadIndexedReferenceObjectsTask

config.detection.minPixels = 20
config.detection.thresholdValue = 5.0
config.detection.includeThresholdMultiplier = 20.0
config.detection.minPixels = 5
config.detection.doTempLocalBackground=True
config.detection.tempLocalBackground.binSize = 32

#Don't make lots of measurements if we can avoid it:
#Dew needed for earlyAstrometry:
for i in [
#        'base_GaussianFlux',
#        'base_SdssShape', #base_SdssShape is needed for PSF determination.
        'base_ScaledApertureFlux',
#        'base_CircularApertureFlux',
        'base_Blendedness',
        'base_LocalBackground',
        'base_Jacobian',
        'base_FPPosition',
        'base_Variance',
        'base_InputCount',
        'base_SkyCoord']:
    config.measurement.plugins[i].doMeasure=False
config.measurement.slots.calibFlux='base_CircularApertureFlux_9_0'
    
config.doEarlyAstrometry=True
from lsst.meas.extensions.astrometryNet import ANetAstrometryTask
config.astrometry.retarget(ANetAstrometryTask)
for source, target in [('B', 'b'), ('G', 'v'), ('R', 'm'), ('L', 'v')]:
    config.astromRefObjLoader.filterMap[source]=target
    config.astrometry.solver.filterMap[source]=target
config.astrometry.solver.useWcsRaDecCenter = True
config.astrometry.solver.useWcsParity = True
config.astrometry.solver.useWcsPixelScale = True
config.astrometry.solver.raDecSearchRadius = 5.
config.astrometry.solver.maxStars = 1000
config.astrometry.solver.catalogMatchDist = 120.
config.astrometry.solver.pixelScaleUncertainty= 1.1
config.astrometry.solver.pixelMargin = 1000
config.astrometry.solver.sipOrder = 3
config.astrometry.solver.calculateSip = True
config.astrometry.solver.maxIter = 20
config.astrometry.solver.matchDistanceSigma = 2.0
config.astrometry.solver.cleaningParameter = 5.0
config.astrometry.rejectThresh = 3.0

#Cosmic rays and background estimation:
config.repair.doCosmicRay = True
config.repair.cosmicray.nCrPixelMax=1000000
config.repair.cosmicray.cond3_fac2 = 0.4

#PSF determination:
config.psfIterations=1
config.measurePsf.starSelector["objectSize"].fluxMin = 1000.
config.measurePsf.starSelector['objectSize'].widthStdAllowed = 10.0
config.measurePsf.starSelector['objectSize'].nSigmaClip = 10.0
config.measurePsf.psfDeterminer.name = "pca"
config.measurePsf.psfDeterminer['pca'].nEigenComponents = 6
config.measurePsf.psfDeterminer['pca'].spatialOrder = 6
config.measurePsf.psfDeterminer['pca'].sizeCellX = 512
config.measurePsf.psfDeterminer['pca'].sizeCellY = 512
config.measurePsf.psfDeterminer['pca'].reducedChi2ForPsfCandidates = 10.0

config.doApCorr = True
config.measureApCorr.refFluxName='base_CircularApertureFlux_6_0'

config.doWrite = False
