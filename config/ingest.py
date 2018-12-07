from lsst.obs.goto.ingest import GotoParseTask
config.parse.retarget(GotoParseTask)

config.parse.translation = {'dataType':'IMGTYPE',
                            'expTime':'EXPTIME',
                            'filter':'FILTER',
                            'field':'OBJECT',
                            'ccd':'UT',
                            'run':'RUN'}

config.parse.translators = {'dateObs':'translateDate',
                            'taiObs':'translateDate',
                            'visit':'translateVisit',
                            'mjd':'translateJd',
                            'survey':'translateSurvey'}

config.register.visit = ['visit', 'run', 'ccd', 'filter', 'dateObs','taiObs']

config.register.unique = ['run', 'ccd', 'filter']

config.register.columns = {'run':'int',
                           'visit':'int',
                           'ccd':'int',
                           'filter':'text',
                           'dataType':'text',
                           'expTime':'double',
                           'dateObs':'text',
                           'taiObs':'text',
                           'mjd':'double',
                           'field':'text',
                           'survey':'text'}

