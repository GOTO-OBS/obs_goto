from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import astropy.units
from lsst.afw.geom import degrees, SpherePoint
from lsst.afw.coord import Observatory, Weather
from lsst.obs.base import MakeRawVisitInfo

__all__ = ["MakeGotoRawVisitInfo"]

class MakeGotoRawVisitInfo(MakeRawVisitInfo):
    """Make a VisitInfo from the FITS header of a GOTO image
    """
    observatory = Observatory(-17.882*degrees, 28.761*degrees, 2332)  # long, lat, elev

    def setArgDict(self, md, argDict):
        """Set an argument dict for makeVisitInfo and pop associated metadata

        @param[in,out] md  metadata, as an lsst.daf.base.PropertyList or PropertySet
        @param[in,out] argdict  a dict of arguments
        """
        argDict["exposureTime"] = self.popFloat(md, 'EXPTIME')

        startDate = self.popIsoDate(md, "DATE-OBS")
        argDict["date"] = self.offsetDate(startDate, 0.5*argDict["exposureTime"])

        argDict["boresightAzAlt"] = SpherePoint(
            self.popAngle(md, "AZ"),
            self.popAngle(md, "ALT"),
        )
        argDict["boresightAirmass"] = self.popFloat(md, "AIRMASS")

        argDict["observatory"] = self.observatory

        argDict['darkTime'] = argDict['exposureTime']
        
#        argDict["boresightRaDec"] = SpherePoint(
#            self.popAngle(md, "RA-TEL", units=astropy.units.h),
#            self.popAngle(md, "DEC-TEL"),
#        )

#        argDict["weather"] = Weather(
#            self.centigradeFromKelvin(self.popFloat(md, "EXT-TEMP")),
#            1.0,
#            self.popFloat(md, "EXT-HUM"),
#        )



