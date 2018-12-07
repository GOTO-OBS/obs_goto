from lsst.obs.goto.printDict  import printDict
import os.path
from lsst.utils import getPackageDir
from lsst.meas.algorithms import LoadIndexedReferenceObjectsTask
from lsst.obs.goto.propagateGotoVisitFlags import PropagateGotoVisitFlagsTask 
#obj = printDict(config, path=['config'])
#quit()

#print('***Lydia***: config/measureCoaddSources.py:' \
#      'Setting doPropagateFlags to False. This could cause problems')

config.match.refObjLoader.ref_dataset_name = "ps1_pv3_3pi_20170110"
for source, target in [('B', 'g'), ('G', 'g'), ('R', 'r'), ('L', 'g')]:
    config.match.refObjLoader.filterMap[source]=target
#config.load(os.path.join(getPackageDir("obs_goto"), "config", "cmodel.py"))
#quit()

config.doMatchSources=False
#config.doWriteMatchesDenormalized = True
config.match.matchRadius=1.0
config.deblend.maxFootprintArea=10000

config.measurement.plugins['base_CircularApertureFlux'].radii=[3.0, 4.5, 6.0, 9.0, 12.0]
config.deblend.propagateAllPeaks = False
config.propagateFlags.retarget(PropagateGotoVisitFlagsTask)
config.doPropagateFlags=True
config.propagateFlags.flags={'calib_psfCandidate': 0.2, 'calib_psfUsed': 0.2, 'calib_psf_reserved': 0.2}
