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

    def translateDate(self, md):

        #start = md.get("UTSTART")
        date = md.get("DATE-OBS")
        start = date[11:]
        date = date.strip()[:10]
        t = Time(date)
        
    #If after midnight, set date to date minus 1 day.
        if int(start.split(":")[0]) < 12:
            date = Time(t.jd-1, format='jd', out_subfmt='date').iso
        
        return date
     
    def translateVisit(self, md):
        visit = md.get("DB-PNT")

        #If no visit number (e.g., flat), revert to the run number.
        if visit == 'NA':
            run = md.get("RUN-ID")
            return int(run.strip('r'))
        else:
            return int(visit)

    def translateCcd(self, md):
        ccd = md.get("INSTRUME")
        return int(ccd.strip('UT'))

