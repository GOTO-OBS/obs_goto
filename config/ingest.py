from lsst.obs.goto.ingest import GotoParseTask
config.parse.retarget(GotoParseTask)

from lsst.obs.goto.printDict  import printDict

#obj = printDict(config, path=['config'])

#print config.register.columns
#quit()

config.parse.translation = {'dataType':'IMGTYPE',
                            'expTime':'EXPTIME',
                            'frameId':'RUN-ID',
                            'filter':'FILTER',
                            'field':'OBJECT'
                           }

config.parse.translators = {'dateObs':'translateDate',
                            'taiObs':'translateDate',
                            'visit':'translateVisit',
                            'ccd':'translateCcd'}

config.register.visit = ['visit', 'ccd', 'filter','dateObs','taiObs']

config.register.unique = ['visit', 'ccd', 'filter']

config.register.columns = {'frameId':'text',
                           'visit':'int',
                           'ccd':'int',
                           'filter':'text',
                           'dataType':'text',
                           'expTime':'double',
                           'dateObs':'text',
                           'taiObs':'text',
                           'field':'text' }

