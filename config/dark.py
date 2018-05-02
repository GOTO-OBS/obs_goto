from lsst.obs.swasp.printDict  import printDict
#from lsst.obs.swasp.isr import SwaspIsrTask

#obj = printDict(config, path=['config'])

#config.isr.retarget(SwaspIsrTask)

print('JRM: config/dark.py: Not repairing cosmic rays') 
config.repair.doCosmicRay=False

#config.darkTime=None

config.visitKeys=['frameId']

#print config.register.columns
#quit()
