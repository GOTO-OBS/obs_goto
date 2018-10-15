#!/usr/bin/env python

'''
Task to perfom forced photometry on a coadded visit frame (i.e., that
made up from all exposures from a visit/ccd combination.

Largely defers to ForcedPhotCcd and ForcedPhotImage, but with its own run function
that allows an exposure to be passed to the function. This feature is useful if one
wants to include forced photometry in a calling script. It still works, however, if
called from the command line with --id's. 
'''

from lsst.meas.base.forcedPhotCcd import ForcedPhotCcdTask, ForcedPhotCcdConfig
import lsst.pipe.base

class ForcedPhotVisitConfig(ForcedPhotCcdConfig):
    pass

class ForcedPhotVisitTask(ForcedPhotCcdTask):

    ConfigClass = ForcedPhotVisitConfig
    RunnerClass = lsst.pipe.base.ButlerInitializedTaskRunner
    _DefaultName = "forcedVisitCcd"
    dataPrefix = "visitCoadd_"

    def run(self, dataRef, exposure=None, psfCache=None):
        
        refWcs = self.references.getWcs(dataRef)
        if exposure is None:
            exposure = self.getExposure(dataRef)
            
        refCat = self.fetchReferences(dataRef, exposure)
        measCat = self.measurement.generateMeasCat(exposure, refCat, refWcs,
                                                   idFactory=self.makeIdFactory(dataRef))
        self.log.info("Performing forced measurement on %s" % (dataRef.dataId,))
        self.attachFootprints(measCat, refCat, exposure, refWcs, dataRef)
        self.measurement.run(measCat, exposure, refCat, refWcs, exposureId=self.getExposureId(dataRef))

        '''
        applyApCorr currently doesn't work; apCorrMap doesn't have a get attribute.
        My suspicion is that an ApCorrMap needs to be created during singleVisitDriver.
        if self.config.doApCorr:
            self.applyApCorr.run(
                catalog=measCat,
                apCorrMap=exposure.getInfo().getApCorrMap()
            )
        '''
        self.catalogCalculation.run(measCat)
        self.writeOutput(dataRef, measCat)

    def _getConfigName(self):
        return "forcedPhotVisit_config"

    def _getMetadataName(self):
        return "visitCoadd_forced_metadata"

