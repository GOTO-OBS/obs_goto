from lsst.obs.goto.printDict  import printDict
#from lsst.ip.diffim.getTemplate import GetCalexpAsTemplateTask

#config.getTemplate.retarget(GetCalexpAsTemplateTask)

#obj = printDict(config, path=['config'])
#quit()
config.doWriteMatchedExp=True


config.refObjLoader.defaultFilter='m'
config.refObjLoader.filterMap={'Clear':'m'}
config.kernelSourcesFromRef=True

config.astrometer.matcher.maxMatchDistArcSec = 60.
config.astrometer.matcher.maxOffsetPix = 300
config.astrometer.matcher.maxRotationDeg = 1.
config.astrometer.wcsFitter.maxScatterArcsec = 40.0

config.astrometer.matcher.maxMatchDistArcSec = 10.
config.astrometer.matcher.maxOffsetPix = 20
config.astrometer.matcher.maxRotationDeg = 1.
config.astrometer.wcsFitter.maxScatterArcsec = 10.0

#Also, need to set how far down in brightness we go down the
#reference catalogue. The default is 50, but this is too low
#for SWasp, as too many are saturated. 100 seems to be ok.
config.astrometer.matcher.numBrightStars = 300
#config.calibrate.photoCal.matcher.numBrightStars = 300
#Sets the default filter to use in the anet reference catalogue:
#config.calibrate.refObjLoader.filterMap['g']='v'
#config.calibrate.refObjLoader.load(os.path.join(getPackageDir("obs_swasp"), "config",
#                                                "filterMap.py")



