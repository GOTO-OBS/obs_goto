import lsst.afw.math as afwMath
from lsst.obs.goto.printDict  import printDict

config.combination.combine=int(afwMath.MEDIAN)
#config.combination.stats.stat=32
config.visitKeys=['visit']
config.isr.doDark=True
config.isr.doDefect=False
#bj = printDict(config, path=['config'])
#quit()
