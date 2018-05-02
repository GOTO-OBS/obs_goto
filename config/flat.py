import lsst.afw.math as afwMath
from lsst.obs.swasp.printDict  import printDict

config.combination.combine=afwMath.MEDIAN
#config.combination.stats.stat=32
config.visitKeys=['frameId']
#config.isr.doDark=False

#bj = printDict(config, path=['config'])
#quit()
