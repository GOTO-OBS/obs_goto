from lsst.obs.goto.ingest import GotoParseTask
config.parse.retarget(GotoParseTask)

from lsst.obs.goto.printDict  import printDict

#obj = printDict(config, path=['config'])

#print config.register.columns
#quit()

config.parse.translation = {'dataType':'IMGTYPE',
                            'expTime':'EXPTIME',
                            'ccd':'INSTRUME',
                            'frameId':'RUN-ID',
                            'visit':'RUN-ID',
                            'filter':'FILTER',
                            'field':'OBJECT'
                           }

config.parse.translators = {'dateObs':'translate_Date',
                            'taiObs':'translate_Date'}

#config.parse.translators = {'visit':'translate_visit'}
                            
config.register.visit = ['visit', 'ccd', 'filter','dateObs','taiObs']

config.register.unique = ['visit', 'ccd', 'filter']

config.register.columns = {'frameId':'text',
                           'visit':'text',
                           'ccd':'text',
                           'filter':'text',
                           'dataType':'text',
                           'expTime':'double',
                           'dateObs':'text',
                           'taiObs':'text',
                           'field':'text' }

#obj = printDict(config, path=['config'])

#print config.register.columns
#quit()
