from lsst.obs.goto.printDict  import printDict
from lsst.ip.diffim.getTemplate import GetCalexpAsTemplateTask

config.getTemplate.retarget(GetCalexpAsTemplateTask)

#obj = printDict(config, path=['config'])
#quit()


config.doWriteMatchedExp=True


config.refObjLoader.defaultFilter='m'
config.refObjLoader.filterMap={'L':'m'}
config.kernelSourcesFromRef= True


config.doSelectSources= True
#config.subtract['zogy'].kernel.name = "AL"
#config.subtract="zogy"



#config.subtract["al"].selectDetection.reEstimateBackground = True
#config.getTemplate.warpType = "psfMatched"
config.astrometer.matcher.maxMatchDistArcSec = 2.
config.astrometer.matcher.maxOffsetPix = 3
config.astrometer.matcher.maxRotationDeg = 1.
config.astrometer.wcsFitter.maxScatterArcsec = 10.0


config.astrometer.matcher.numBrightStars = 300


