from lsst.obs.goto.ingest import GotoParseTask
config.parse.retarget(GotoParseTask)

from lsst.obs.goto.printDict  import printDict

config.parse.translation = {'dataType':'IMGTYPE',
                            'expTime':'EXPTIME',
                            'filter':'FILTER',
                            'field':'OBJECT',
                            'ccd':'UT',
                            'run':'RUN',
                            'visit':'DB-EXPS'}

config.parse.translators = {'dateObs':'translateDate',
                            'taiObs':'translateDate',
                            'visit':'translateVisit'}

config.register.visit = ['visit', 'run', 'ccd', 'filter', 'dateObs','taiObs']

config.register.unique = ['run', 'ccd']

config.register.columns = {'run':'int',
                           'visit':'int',
                           'ccd':'int',
                           'filter':'text',
                           'dataType':'text',
                           'expTime':'double',
                           'dateObs':'text',
                           'taiObs':'text',
                           'field':'text'}

