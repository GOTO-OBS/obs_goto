#Import the library to parse the clibrations:
from lsst.obs.goto.ingest import GotoCalibsParseTask
config.parse.retarget(GotoCalibsParseTask)

#These are the columns that appear in calibregistry.sqlite3:
config.register.columns = {'ccd': 'int',
                           'filter': 'text',
                           'calibDate': 'text',
                           'validStart': 'text',
                           'validEnd': 'text'}

#If the values in the header aren't in the format you wish, you
#can use a translator (defined in SwaspCalibParseTask).
config.parse.translators = {'ccd': 'translate_ccd',
                            'filter': 'translate_filter',
                            'calibDate': 'translate_calibDate'}

#The combination of these columns must identify the entry uniquely:
config.register.unique = ['filter', 'ccd', 'calibDate']

#The tables contained within the registry:
config.register.tables = ['bias', 'dark', 'flat']

#I'm not sure what 'visit' is used for, but there must be at least
#one common element between unique and visit.
config.register.visit = ['calibDate', 'filter']

#config.clobber = True
