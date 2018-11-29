#
# LSST Data Management System
# Copyright 2008, 2009, 2010, 2011, 2012 LSST Corporation.
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

import lsst.pipe.base as pipeBase
from lsst.pipe.tasks.coaddHelpers import groupPatchExposures, getGroupDataRef
from lsst.pipe.tasks.makeCoaddTempExp import MakeCoaddTempExpTask

class GotoMakeCoaddTempExpTask(MakeCoaddTempExpTask):

    @pipeBase.timeMethod
    def run(self, patchRef, selectDataList=[]):
        """
        This does the same job as MakeCoaddTempExp (so see that header for more information)
        but we've had to change the visitid from "visit" to "run" as GOTO uses the latter 
        as the unique identifyer. This change is also reflected in propogateGotoVisitFlags.py 
        """
        skyInfo = self.getSkyInfo(patchRef)

        # DataRefs to return are of type *_directWarp unless only *_psfMatchedWarp requested
        if self.config.makePsfMatched and not self.config.makeDirect:
            primaryWarpDataset = self.getTempExpDatasetName("psfMatched")
        else:
            primaryWarpDataset = self.getTempExpDatasetName("direct")

        calExpRefList = self.selectExposures(patchRef, skyInfo, selectDataList=selectDataList)
        if len(calExpRefList) == 0:
            self.log.warn("No exposures to coadd for patch %s", patchRef.dataId)
            return None
        self.log.info("Selected %d calexps for patch %s", len(calExpRefList), patchRef.dataId)
        calExpRefList = [calExpRef for calExpRef in calExpRefList if calExpRef.datasetExists("calexp")]
        self.log.info("Processing %d existing calexps for patch %s", len(calExpRefList), patchRef.dataId)

        groupData = groupPatchExposures(patchRef, calExpRefList, self.getCoaddDatasetName(),
                                        primaryWarpDataset)
        self.log.info("Processing %d warp exposures for patch %s", len(groupData.groups), patchRef.dataId)

        dataRefList = []
        for i, (tempExpTuple, calexpRefList) in enumerate(groupData.groups.items()):
            tempExpRef = getGroupDataRef(patchRef.getButler(), primaryWarpDataset,
                                         tempExpTuple, groupData.keys)
            if self.reuse and tempExpRef.datasetExists(datasetType=primaryWarpDataset, write=True):
                self.log.info("Skipping makeCoaddTempExp for %s; output already exists.", tempExpRef.dataId)
                dataRefList.append(tempExpRef)
                continue
            self.log.info("Processing Warp %d/%d: id=%s", i, len(groupData.groups), tempExpRef.dataId)

            # TODO: mappers should define a way to go from the "grouping keys" to a numeric ID (#2776).
            # For now, we try to get a long integer "visit" key, and if we can't, we just use the index
            # of the visit in the list.

            #JRM: This is the only thing that differs from the standard
            #makeCoaddTempExp...
            try:
                visitId = int(tempExpRef.dataId["run"])                
            except (KeyError, ValueError):
                visitId = i

            exps = self.createTempExp(calexpRefList, skyInfo, visitId).exposures

            if any(exps.values()):
                dataRefList.append(tempExpRef)
            else:
                self.log.warn("Warp %s could not be created", tempExpRef.dataId)

            if self.config.doWrite:
                for (warpType, exposure) in exps.items():  # compatible w/ Py3
                    if exposure is not None:
                        self.log.info("Persisting %s" % self.getTempExpDatasetName(warpType))
                        tempExpRef.put(exposure, self.getTempExpDatasetName(warpType))

        return dataRefList

