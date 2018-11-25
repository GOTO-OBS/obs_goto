from lsst.obs.goto.printDict  import printDict
import os.path
from lsst.utils import getPackageDir
from lsst.meas.algorithms import LoadIndexedReferenceObjectsTask
#obj = printDict(config, path=['config'])
#quit()

#print('***Lydia***: config/measureCoaddSources.py:' \
#      'Setting doPropagateFlags to False. This could cause problems')
config.doPropagateFlags=True
config.propagateFlags.flags={'calib_psfCandidate': 0.2, 'calib_psfUsed': 0.2, 'calib_psf_reserved': 0.2}

config.match.refObjLoader.ref_dataset_name = "ps1_pv3_3pi_20170110"
for source, target in [('B', 'g'), ('G', 'g'), ('R', 'r'), ('L', 'g')]:
    config.match.refObjLoader.filterMap[source]=target
#config.load(os.path.join(getPackageDir("obs_goto"), "config", "cmodel.py"))
#quit()

config.doMatchSources=False
#config.doWriteMatchesDenormalized = True
config.match.matchRadius=1.0
config.deblend.maxFootprintArea=1000000

