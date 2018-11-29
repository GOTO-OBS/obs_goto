#!/usr/bin/env python
#
# LSST Data Management System
# Copyright 2014-2015 LSST/AURA
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
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.    See the
# GNU General Public License for more details.
#
# You should have received a copy of the LSST License Statement and
# the GNU General Public License along with this program.  If not,
# see <http://www.lsstcorp.org/LegalNotices/>.
#
import numpy
from lsst.pex.config import Config, Field, DictField
from lsst.pipe.base import Task
import lsst.afw.geom as afwGeom
import lsst.afw.table as afwTable
from lsst.pipe.tasks.propagateVisitFlags import PropagateVisitFlagsTask

class PropagateGotoVisitFlagsTask(PropagateVisitFlagsTask):
    def run(self, butler, coaddSources, ccdInputs, coaddWcs):
        """
        """
        
        if len(self.config.flags) == 0:
            return

        flags = self._keys.keys()
        visitKey = ccdInputs.schema.find("visit").key
        ccdKey = ccdInputs.schema.find("ccd").key
        radius = self.config.matchRadius*afwGeom.arcseconds

        self.log.info("Propagating flags %s from inputs" % (flags,))

        counts = dict((f, numpy.zeros(len(coaddSources), dtype=int)) for f in flags)
        indices = numpy.array([s.getId() for s in coaddSources])  # Allowing for non-contiguous data

        # Accumulate counts of flags being set
        for ccdRecord in ccdInputs:
            v = ccdRecord.get(visitKey)
            c = ccdRecord.get(ccdKey)
            ccdSources = butler.get("src", run=int(v), ccd=int(c), immediate=True)
            for sourceRecord in ccdSources:
                sourceRecord.updateCoord(ccdRecord.getWcs())
            for flag in flags:
                # We assume that the flags will be relatively rare, so it is more efficient to match
                # against a subset of the input catalog for each flag than it is to match once against
                # the entire catalog.  It would be best to have built a kd-tree on coaddSources and
                # keep reusing that for the matching, but we don't have a suitable implementation.
                mc = afwTable.MatchControl()
                mc.findOnlyClosest = False
                matches = afwTable.matchRaDec(coaddSources, ccdSources[ccdSources.get(flag)], radius, mc)
                for m in matches:
                    index = (numpy.where(indices == m.first.getId()))[0][0]
                    counts[flag][index] += 1

        # Apply threshold
        for f in flags:
            key = self._keys[f]
            for s, num in zip(coaddSources, counts[f]):
                numOverlaps = len(ccdInputs.subsetContaining(s.getCentroid(), coaddWcs, True))
                s.setFlag(key, bool(num > numOverlaps*self.config.flags[f]))
            self.log.info("Propagated %d sources with flag %s" % (sum(s.get(key) for s in coaddSources), f))
