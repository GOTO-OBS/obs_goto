from lsst.ip.diffim.getTemplate import GetCalexpAsTemplateTask

config.getTemplate.retarget(GetCalexpAsTemplateTask)

#What to do:
config.doSelectSources = True
config.doSubtract = True
config.doPreConvolve = False
config.useGaussianForPreConvolution = True
config.doDetection = True
config.doMerge = False
config.doMeasurement = False
config.doDipoleFitting = False
config.doForcedMeasurement = False
config.doWriteSubtractedExp = True
config.doWriteMatchedExp = True
config.doWriteSources = False
config.doSpatiallyVarying = True

#Reference catalogue for registration
config.refObjLoader.ref_dataset_name='ps1_pv3_3pi_20170110_GmagLT19'
config.refObjLoader.defaultFilter='g'
config.refObjLoader.filterMap={'L': 'g'}

#Source selector for PSF canidates
#Using the same parameters as in processCcd.characterizeImage:
config.sourceSelector.widthStdAllowed = 10.0
config.sourceSelector.nSigmaClip = 10.0

config.subtract.name='al'

# Size (rows) in pixels of each SpatialCell for spatial modeling
config.subtract['al'].kernel['AL'].sizeCellX=256
config.subtract['al'].kernel['AL'].sizeCellY=256

config.subtract['al'].kernel['AL'].kernelSize=35
config.subtract['al'].kernel['AL'].kernelSizeMin=35
config.subtract['al'].kernel['AL'].kernelSizeMax=51

config.subtract['al'].kernel['AL'].candidateResidualMeanMax=10.
config.subtract['al'].kernel['AL'].candidateResidualStdMax=10.

config.detection.minPixels = 5
config.detection.thresholdValue=10.

config.kernelSourcesFromRef=False