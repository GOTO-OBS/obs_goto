import os.path
from lsst.utils import getPackageDir
from lsst.meas.algorithms import ColorLimit

configDir = os.path.join(getPackageDir("obs_goto"), "config")

#Detection:
config.detection.thresholdValue = 30.0
config.detection.minPixels = 10
config.detection.isotropicGrow = True
config.detection.doTempLocalBackground=True
config.detection.tempLocalBackground.binSize = 32
config.measurement.slots.calibFlux='base_CircularApertureFlux_9_0'

#Deblending
config.doDeblend = True
config.deblend.maxFootprintSize = 0
config.deblend.maxFootprintArea = 10000

#Measurement:
for i in [
        #'base_GaussianFlux', #Needed for PSF in imageDifference.py
        #'base_SdssShape',    #Needed for shape information for 4th-year project
        'base_ScaledApertureFlux',
        #'base_CircularApertureFlux', #Needed for zeropoint
        'base_Blendedness',
        'base_LocalBackground',
        'base_Jacobian',
        'base_FPPosition',
        'base_Variance',
        'base_InputCount',
        #'base_SkyCoord',#Needed for zeropoint
        ]: 
    config.measurement.plugins[i].doMeasure=False

#Astrometry
config.astrometry.forceKnownWcs = False
config.doAstrometry = True

from lsst.meas.extensions.astrometryNet import ANetAstrometryTask
config.astrometry.retarget(ANetAstrometryTask)
from lsst.meas.extensions.astrometryNet import LoadAstrometryNetObjectsTask
config.astromRefObjLoader.retarget(LoadAstrometryNetObjectsTask)

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

#Photometric calibration:
#JRM:
#config.doPhotoCal = True
config.doPhotoCal = False
#####
config.photoCal.match.matchRadius = 1.24
config.photoCal.colorterms.load(os.path.join(configDir, 'colorterms.py'))
#config.photoCal.applyColorTerms = True
config.photoCal.applyColorTerms = False
config.photoCal.match.referenceSelection.doMagLimit = True
config.photoCal.match.referenceSelection.magLimit.fluxField = "i_flux"
config.photoCal.match.referenceSelection.magLimit.maximum = 19.0
config.photoCal.match.referenceSelection.magLimit.minimum = 11.0

colors = config.photoCal.match.referenceSelection.colorLimits
colors["r-i"] = ColorLimit(primary="r_flux", secondary="i_flux", maximum=0.5)
colors["g-r"] = ColorLimit(primary="g_flux", secondary="r_flux", minimum=0.0)

from lsst.meas.algorithms import LoadIndexedReferenceObjectsTask
config.photoRefObjLoader.retarget(LoadIndexedReferenceObjectsTask)
#config.photoRefObjLoader.ref_dataset_name = "ps1_pv3_3pi_20170110_GmagLT19"
for source, target in [('B', 'g'), ('G', 'g'), ('R', 'r'), ('L', 'g')]:
    config.photoRefObjLoader.filterMap[source]=target
#config.photoCal.photoCatName = "ps1_pv3_3pi_20170110_GmagLT19"    

#Caliculate aperture correction?:
config.doApCorr = True

#Match to external catalog?
config.doWriteMatches = False
