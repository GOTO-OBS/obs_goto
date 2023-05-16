from lsst.obs.base import FitsRawFormatterBase
from ._instrument import North1,North2
from .gotoFilters import GOTO_FILTER_DEFINITIONS
# Comment-out the following line if you put .translators/necam.py in the
# astro_metadata_translator repository:
from .translators import GotoTranslator
# ...and uncomment the following:
# from astro_metadata_translator import NeCamTranslator

class GotoRawFormatter(FitsRawFormatterBase):
    """
    Gen3 Butler formatter for Goto raw data.
    """
    translatorClass = GotoTranslator
    filterDefinitions = GOTO_FILTER_DEFINITIONS

    def getDetector(self, id):
        return NotImplementedError()

class North1RawFormatter(GotoRawFormatter):

    def getDetector(self, id):
        return North1().getCamera()[id]

class North2RawFormatter(GotoRawFormatter):

    def getDetector(self, id):
        return North2().getCamera()[id]
