from lsst.pipe.tasks.ingestCalibs import CalibsParseTask
from lsst.pipe.tasks.ingest import ParseTask
from astropy.time import Time
import re

class GotoCalibsParseTask(CalibsParseTask):

    def getInfo(self, filename):
        """Get information about the image from the filename and/or its contents.
        """
        phuInfo, infoList = CalibsParseTask.getInfo(self, filename)
        # Single-extension fits without EXTNAME can be a valid CP calibration product
        # Use info of primary header unit
        if not infoList:
            infoList.append(phuInfo)
        for info in infoList:
            info['path'] = filename
        return phuInfo, infoList

    def _translateFromCalibId(self, field, md):
        data = md.get("CALIB_ID")
        match = re.search(".*%s=(\S+)" % field, data)
        return match.groups()[0]

    def translate_ccd(self, md):
        
        if md.exists("CALIB_ID"):
            return self._translateFromCalibId("ccd", md)
        else:
            return 1

    def translate_filter(self, md):
        
        if md.exists("CALIB_ID"):
            return self._translateFromCalibId("filter", md)
        else:
            return "L"

    def translate_calibDate(self, md):
        
        if md.exists("CALIB_ID"):
            return self._translateFromCalibId("calibDate", md)
        else:
            return "2019-02-22"

class GotoParseTask(ParseTask):

    def translateDate(self, md):

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

    def translateJd(self, md):
        date = self.translateDate(md)
        t = Time(date, format='iso')
        return int(t.mjd)

    def translateSurvey(self, md):
        tileName = md.get('TILENAME')
        event = md.get('EVENT')
        if (tileName != 'NA') and (event == 'NA'):
            return 'T'
        else:
            return 'F'
