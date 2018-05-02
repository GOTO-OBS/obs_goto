#
# LSST Data Management System
# Copyright 2016 LSST Corporation.
#
# This product includes software developed by the
# LSST Project (http://www.lsst.org/).
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the LSST License Statement and
# the GNU General Public License along with this program.  If not,
# see <http://www.lsstcorp.org/LegalNotices/>.
#
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import astropy.units

from lsst.afw.geom import degrees, SpherePoint
from lsst.afw.coord import Observatory, Weather
from lsst.obs.base import MakeRawVisitInfo

__all__ = ["MakeGotoRawVisitInfo"]


class MakeGotoRawVisitInfo(MakeRawVisitInfo):
    """Make a VisitInfo from the FITS header of a Subaru HSC image

    Boresight rotation angle could probably be set from one of:
    - INST-PT (but apparently only available for HSC, not suprimecam)
    - INR-TR, INR-END (but appears to not be SKY; so probably not interesting)
    """
    observatory = Observatory(-17.882*degrees, 28.761*degrees, 2332)  # long, lat, elev

    def setArgDict(self, md, argDict):
        """Set an argument dict for makeVisitInfo and pop associated metadata

        @param[in,out] md  metadata, as an lsst.daf.base.PropertyList or PropertySet
        @param[in,out] argdict  a dict of arguments
        """
        MakeRawVisitInfo.setArgDict(self, md, argDict)
        argDict["boresightRaDec"] = SpherePoint(
            self.popAngle(md, "RA2000", units=astropy.units.h),
            self.popAngle(md, "DEC2000"),
        )
#        argDict["boresightAzAlt"] = Coord(
#            self.popAngle(md, "AZIMUTH"),
#            self.popAngle(md, "ALTITUDE"),
#        )
        argDict["boresightAirmass"] = self.popFloat(md, "AIRMASS")
        argDict["observatory"] = self.observatory
        argDict["weather"] = Weather(
            self.centigradeFromKelvin(self.popFloat(md, "OUT-TMP")),
            self.pascalFromMmHg(self.popFloat(md, "OUT-PRS")),
            self.popFloat(md, "OUT-HUM"),
        )
        LST = self.popAngle(md, "LST-STR", units=astropy.units.h)
        argDict['era'] = self.eraFromLstAndLongitude(LST, self.observatory.getLongitude())
        argDict['darkTime'] = argDict['exposureTime']

    def getDateAvg(self, md, exposureTime):
        """Return date at the middle of the exposure

        @param[in,out] md  FITS metadata; changed in place
        @param[in] exposureTime  exposure time in sec
        """
        startDate = self.popMjdDate(md, "MJD-STR")
        return self.offsetDate(startDate, 0.5*exposureTime)
