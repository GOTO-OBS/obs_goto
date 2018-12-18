import os.path
from lsst.utils import getPackageDir
from lsst.meas.algorithms import ColorLimit
from lsst.meas.algorithms import LoadIndexedReferenceObjectsTask

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

#Astrometry (now solved in GotoCharTask)
config.astrometry.forceKnownWcs = True
config.doAstrometry = False

#Photometric calibration:
config.doPhotoCal = True
config.photoCal.match.matchRadius = 1.24
config.photoCal.colorterms.load(os.path.join(configDir, 'colorterms.py'))
config.photoCal.applyColorTerms = True
config.photoCal.match.referenceSelection.doMagLimit = True
config.photoCal.match.referenceSelection.magLimit.fluxField = "i_flux"
config.photoCal.match.referenceSelection.magLimit.maximum = 19.0
config.photoCal.match.referenceSelection.magLimit.minimum = 13.0

colors = config.photoCal.match.referenceSelection.colorLimits
colors["r-i"] = ColorLimit(primary="r_flux", secondary="i_flux", maximum=0.5)
colors["g-r"] = ColorLimit(primary="g_flux", secondary="r_flux", minimum=0.0)

config.photoRefObjLoader.retarget(LoadIndexedReferenceObjectsTask)
config.photoRefObjLoader.ref_dataset_name = "ps1_pv3_3pi_20170110"
for source, target in [('B', 'g'), ('G', 'g'), ('R', 'r'), ('L', 'g')]:
    config.photoRefObjLoader.filterMap[source]=target
config.photoCal.photoCatName = "ps1_pv3_3pi_20170110"    

#Caliculate aperture correction?:
config.doApCorr = True

#Match to external catalog?
config.doWriteMatches = False
