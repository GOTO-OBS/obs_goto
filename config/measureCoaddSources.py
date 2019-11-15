import os.path
from lsst.utils import getPackageDir
from lsst.obs.goto.propagateGotoVisitFlags import PropagateGotoVisitFlagsTask 

#Match to reference catalogue? In this case PanStarrs:
config.doMatchSources=False
config.match.matchRadius=1.0
config.match.refObjLoader.ref_dataset_name = "ps1_pv3_3pi_20170110"
for source, target in [('B', 'g'),
                       ('G', 'g'),
                       ('R', 'r'),
                       ('L', 'g')]:
    config.match.refObjLoader.filterMap[source]=target

#CModel is quite slow and now configured properly yet.
#We'll want to turn it on in the future.
#config.load(os.path.join(getPackageDir("obs_goto"), "config", "cmodel.py"))

config.measurement.plugins['base_CircularApertureFlux'].radii=[3.0, 4.5, 6.0, 9.0, 12.0,24.0,48.0]
config.measurement.load(os.path.join(getPackageDir("obs_goto"), "config", "kron.py"))

#This is needed as we use 'run' rather than visit:
config.propagateFlags.retarget(PropagateGotoVisitFlagsTask)

#Propogate flags from calexps?
config.doPropagateFlags=True
config.propagateFlags.flags={'calib_psf_candidate': 0.2,
                             'calib_psf_used': 0.2,
                             'calib_psf_reserved': 0.2}
