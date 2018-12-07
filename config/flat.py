import lsst.afw.math as afwMath

config.combination.combine=int(afwMath.MEDIAN)
config.visitKeys=['visit']
config.isr.doDark=True
config.isr.doDefect=False
config.isr.doAddDistortionModel = False

