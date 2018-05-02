from lsst.obs.goto.ingest import GotoParseTask
config.parse.retarget(GotoParseTask)

from lsst.obs.goto.printDict  import printDict

config.parse.translation = {'dataType':'IMGTYPE',
                            'expTime':'EXPTIME',
                            'ccd':'INSTRUME',
                            'frameId':'RUN',
                            'filter':'FILTER',
                            'dateObs':'DATE-OBS',
                            'taiObs':'DATE-OBS'
                           }

#config.parse.translators = {'dateObs':'translate_Date',
#                            'taiObs':'translate_Date'}

config.parse.translators = {'visit':'translate_visit'}
                            
config.register.visit = ['visit', 'frameId', 'ccd', 'filter']

config.register.unique = ['visit', 'ccd', 'filter']

config.register.columns = {'frameId':'text',
                           'visit':'text',
                           'ccd':'text',
                           'filter':'text',
                           'dataType':'text',
                           'expTime':'double',
                           'dateObs':'text',
                           'taiObs':'text'}

#obj = printDict(config, path=['config'])

#print config.register.columns
#quit()
