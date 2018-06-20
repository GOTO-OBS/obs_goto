from lsst.obs.goto.printDict  import printDict
from lsst.ip.diffim.getTemplate import GetCalexpAsTemplateTask

config.getTemplate.retarget(GetCalexpAsTemplateTask)

#obj = printDict(config, path=['config'])
#quit()


config.doWriteMatchedExp=True

#config.doUseRegister=True
#config.doDebugRegister=True
#config.register.matchRadius=1.


config.refObjLoader.defaultFilter='m'
config.refObjLoader.filterMap={'L':'v'}

config.doSelectSources= True
config.kernelSourcesFromRef=True

#config.subtract["al"].selectDetection.reEstimateBackground = True
#config.getTemplate.warpType = "psfMatched"

config.astrometer.matcher.maxMatchDistArcSec = 2.
config.astrometer.wcsFitter.maxScatterArcsec = 10.0

config.detection.minPixels = 5

#config.doPreConvolve=True

#config.subtract['zogy'].kernel.name = "AL"
#config.subtract="zogy"
#config.subtract['zogy'].zogyConfig.inImageSpace=True


