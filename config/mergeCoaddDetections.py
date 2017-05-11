from lsst.obs.goto.printDict  import printDict

obj = printDict(config, path=['config'])
config.priorityList = ["m","Clear"]

