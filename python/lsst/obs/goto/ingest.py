from lsst.pipe.tasks.ingestCalibs import CalibsParseTask
#from lsst.pipe.tasks.ingest import IngestTask, ParseTask, IngestArgumentParser
from lsst.pipe.tasks.ingest import ParseTask
from astropy.time import Time
import re

class GotoCalibsParseTask(CalibsParseTask):

    def _translateFromCalibId(self, field, md):
        data = md.get("CALIB_ID")
        match = re.search(".*%s=(\S+)" % field, data)
        return match.groups()[0]

    def translate_ccd(self, md):
        return self._translateFromCalibId("ccd", md)
    
    def translate_filter(self, md):
        return self._translateFromCalibId("filter", md)
    
    def translate_calibDate(self, md):
        return self._translateFromCalibId("calibDate", md)
    
class GotoParseTask(ParseTask):

    def translate_Date(self, md):

        start = md.get("UTSTART")
        date = md.get("DATE-OBS")

        t = Time(date)
        
    #If after midnight, set date to date minus 1 day.
    #    if int(start.split(":")[0]) < 12:
     #       date = Time(t.jd-1, format='jd', out_subfmt='date').iso
            
        return date
     
    def translate_visit(self, md):

        frame = md.get("RUN")
        date = md.get("DATE-OBS")

        visit = date + frame

        return visit
