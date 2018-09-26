from lsst.obs.goto.printDict  import printDict
from lsst.pipe.tasks.selectImages import PsfWcsSelectImagesTask

#config.assembleCoadd.select.retarget(PsfWcsSelectImagesTask)
#config.select.retarget(PsfWcsSelectImagesTask)

#config.detectCoaddSources.detection.background.binSize=4000

#config.makeCoaddTempExp.makePsfMatched = True
#config.makeCoaddTempExp.doPsfMatch = True

#Detection can be slow, especially if measuring a lot of parameters.
#Can turn on when creating deep catalogues.
config.doDetection = True
