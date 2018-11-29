#Calibrate configs:
import os.path
from lsst.utils import getPackageDir
from lsst.meas.algorithms import ColorLimit
from lsst.meas.algorithms import LoadIndexedReferenceObjectsTask

configDir = os.path.join(getPackageDir("obs_goto"), "config")

for i in [
        #'base_GaussianFlux', Needed for PSF in imageDifference.py
        'base_SdssShape',
        'base_ScaledApertureFlux',
        #'base_CircularApertureFlux', Needed for zeropoint
        'base_Blendedness',
        'base_LocalBackground',
        'base_Jacobian',
        'base_FPPosition',
        'base_Variance',
        'base_InputCount',
        #'base_SkyCoord', Needed for zeropoint
        ]:
    config.measurement.plugins[i].doMeasure=False

config.doAstrometry = False
config.astrometry.forceKnownWcs = True
config.doPhotoCal = True

config.detection.threshold = 20.

colors = config.photoCal.match.referenceSelection.colorLimits
config.photoCal.colorterms.load(os.path.join(configDir, 'colorterms.py'))
config.photoCal.applyColorTerms = True

config.photoCal.match.referenceSelection.doMagLimit = True
config.photoCal.match.referenceSelection.magLimit.fluxField = "i_flux"
colors["r-i"] = ColorLimit(primary="r_flux", secondary="i_flux", maximum=0.5)
colors["g-r"] = ColorLimit(primary="g_flux", secondary="r_flux", minimum=0.0)
config.photoCal.match.referenceSelection.magLimit.maximum = 19.0
config.photoCal.match.referenceSelection.magLimit.minimum = 13.0

config.photoRefObjLoader.retarget(LoadIndexedReferenceObjectsTask)
config.photoRefObjLoader.ref_dataset_name = "ps1_pv3_3pi_20170110"

for source, target in [('B', 'g'), ('G', 'g'), ('R', 'r'), ('L', 'g')]:
    config.photoRefObjLoader.filterMap[source]=target
    
config.photoCal.photoCatName = "ps1_pv3_3pi_20170110"
config.doApCorr = False
