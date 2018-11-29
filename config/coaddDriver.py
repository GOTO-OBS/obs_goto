from lsst.obs.goto.printDict  import printDict
from lsst.pipe.tasks.selectImages import PsfWcsSelectImagesTask
from lsst.obs.goto.makeGotoCoaddTempExp import GotoMakeCoaddTempExpTask

config.makeCoaddTempExp.retarget(GotoMakeCoaddTempExpTask)
#config.assembleCoadd.select.retarget(PsfWcsSelectImagesTask)
#config.select.retarget(PsfWcsSelectImagesTask)

#config.detectCoaddSources.detection.background.binSize=4000

#config.makeCoaddTempExp.makePsfMatched = True
#config.makeCoaddTempExp.doPsfMatch = True

#Detection can be slow, especially if measuring a lot of parameters.
#Can turn on when creating deep catalogues.
config.doDetection = False
config.detectCoaddSources.detection.minPixels = 10
config.detectCoaddSources.detection.background.binSize=8192
config.detectCoaddSources.detection.tempLocalBackground.binSize=32
config.detectCoaddSources.detection.tempWideBackground.binSize=1024
