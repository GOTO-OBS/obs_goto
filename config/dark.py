from lsst.obs.goto.printDict  import printDict

#obj = printDict(config, path=['config'])
#quit()
print('JRM: config/dark.py: Not repairing cosmic rays') 
config.repair.doCosmicRay=False

#config.darkTime=None

config.visitKeys=['visit']
config.isr.doDefect=False
config.isr.doAddDistortionModel = False
#print config.register.columns
#quit()
