from lsst.ip.diffim.getTemplate import GetCalexpAsTemplateTask

#config.getTemplate.retarget(GetCalexpAsTemplateTask)

config.doWriteMatchedExp=True

#config.doUseRegister=True
#config.doDebugRegister=True
#config.register.matchRadius=1.

config.refObjLoader.defaultFilter='m'
config.refObjLoader.filterMap={'L':'v'}

config.doSelectSources= True
config.doDetection = True
config.doMeasurement = True
config.doDipoleFitting = False
config.doWriteSources = True
config.doMerge = True
config.doPreConvolve = True
config.doDecorrelation = True

config.kernelSourcesFromRef=True

#config.subtract["al"].selectDetection.reEstimateBackground = True
#config.getTemplate.warpType = "psfMatched"

#config.astrometer.matcher.maxMatchDistArcSec = 2.
#config.astrometer.wcsFitter.maxScatterArcsec = 10.0
#config.astrometer.matcher.numBrightStars=500

config.detection.minPixels = 5

config.sourceSelector.fluxMin = 1000.0
config.sourceSelector.fluxMax = 0

config.sourceSelector.widthMin = 1.0
config.sourceSelector.widthMax = 4.0
config.sourceSelector.widthStdAllowed = 4.0
config.sourceSelector.nSigmaClip = 3.0

config.subtract['al'].kernel['AL'].spatialKernelOrder = 3

# Number of Gaussians in alard-lupton basis
config.subtract['al'].kernel['AL'].alardNGauss = 2

# Polynomial order of spatial modification of Gaussians.  Must in number equal alardNGauss
config.subtract['al'].kernel['AL'].alardDegGauss = [4,2]

# Sigma in pixels of Gaussians (FWHM = 2.35 sigma).  Must in number equal alardNGauss
config.subtract['al'].kernel['AL'].alardSigGauss = [1.0,2.0]

config.detection.minPixels = 5
config.detection.thresholdValue=5.5

#config.subtract['zogy'].kernel.name = "AL"
#config.subtract="zogy"
#config.subtract['zogy'].zogyConfig.inImageSpace=True


