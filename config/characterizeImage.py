from lsst.meas.algorithms import LoadIndexedReferenceObjectsTask

config.detection.minPixels = 20
config.detection.thresholdValue = 5.0
config.detection.includeThresholdMultiplier = 20.0
config.detection.minPixels = 5
config.detection.doTempLocalBackground=True
config.detection.tempLocalBackground.binSize = 32

#Don't make lots of measurements if we can avoid it:
#Few needed for earlyAstrometry:
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

#Cosmic rays and background estimation:
#We need a low value for cond3_fac2 to prevent the cores
#of stars from being identified as cosmic rays see:
#Section 4.4 of Bosch18: https://doi.org/10.1093/pasj/psx080
config.repair.doCosmicRay = True
config.repair.cosmicray.nCrPixelMax=100000
config.repair.cosmicray.cond3_fac2 = 0.1

#PSF determination:
config.measurePsf.starSelector['objectSize'].widthStdAllowed = 10.0
config.measurePsf.starSelector['objectSize'].nSigmaClip = 10.0

#Using PCA:
#config.measurePsf.psfDeterminer.name = "pca"
#config.measurePsf.psfDeterminer['pca'].nEigenComponents = 6
#config.measurePsf.psfDeterminer['pca'].spatialOrder = 2
#config.measurePsf.psfDeterminer['pca'].sizeCellX = 512
#config.measurePsf.psfDeterminer['pca'].sizeCellY = 512
#config.measurePsf.psfDeterminer['pca'].reducedChi2ForPsfCandidates = 50.0
#config.measurePsf.psfDeterminer['pca'].spatialReject = 50.0

#Using PSFEx:
import lsst.meas.extensions.psfex.psfexPsfDeterminer
config.measurePsf.psfDeterminer.name='psfex'
config.measurePsf.psfDeterminer['psfex'].spatialOrder = 3
config.measurePsf.psfDeterminer['psfex'].recentroid = True
config.measurePsf.psfDeterminer['psfex'].psfexBasis = 'PIXEL_AUTO'
config.measurePsf.psfDeterminer['psfex'].samplingSize = 0.0

config.doApCorr = True
config.measureApCorr.refFluxName='base_CircularApertureFlux_6_0'

config.doWrite = False
