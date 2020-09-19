#This is needed as we use 'run' instead of 'visit':
from lsst.obs.goto.makeGotoCoaddTempExp import GotoMakeCoaddTempExpTask
config.makeCoaddTempExp.retarget(GotoMakeCoaddTempExpTask)

#Uncomment this if we want to select frames based on PSF:
#from lsst.pipe.tasks.selectImages import PsfWcsSelectImagesTask
#config.assembleCoadd.select.retarget(PsfWcsSelectImagesTask)

#Detection can be slow, especially if measuring a lot of parameters.
#Can turn on when creating deep catalogues.
config.doDetection = False
config.detectCoaddSources.detection.minPixels = 10
config.detectCoaddSources.detection.background.binSize=8192
config.detectCoaddSources.detection.tempLocalBackground.binSize=32
config.detectCoaddSources.detection.tempWideBackground.binSize=1024
