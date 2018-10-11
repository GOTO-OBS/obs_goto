#!/usr/bin/env python

'''
Task to perfom forced photometry on a coadded visit frame (i.e., that
made up from all exposures from a visit/ccd combination.

Largely defers to ForcedPhotCcd and ForcedPhotImage, but with its own run function
that allow an exposure to be passed to the function. This feature is useful if one
wants to include forced photometry in a calling script.
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
        import pdb
        pdb.set_trace()
        refWcs = self.references.getWcs(dataRef)
        if exposure is None:
            exposure = self.getExposure(dataRef)
            
        refCat = self.fetchReferences(dataRef, exposure)
        measCat = self.measurement.generateMeasCat(exposure, refCat, refWcs,
                                                   idFactory=self.makeIdFactory(dataRef))
        self.log.info("Performing forced measurement on %s" % (dataRef.dataId,))
        self.attachFootprints(measCat, refCat, exposure, refWcs, dataRef)
        self.measurement.run(measCat, exposure, refCat, refWcs, exposureId=self.getExposureId(dataRef))

        if self.config.doApCorr:
            self.applyApCorr.run(
                catalog=measCat,
                apCorrMap=exposure.getInfo().getApCorrMap()
            )
        self.catalogCalculation.run(measCat)
        self.writeOutput(dataRef, measCat)


    def _getConfigName(self):
        return self.dataPrefix + "forcedPhot_config"

    def _getMetaDataName(self):
        return self.dataPrefix + "forcedPhot_metadata"
'''
    def getSchemaCatalogs(self):
        """!Get a dict of Schema catalogs that will be used by this Task.
        In the case of forced taks, there is only one schema for each type of forced measurement.
        The dataset type for this measurement is defined in the mapper.
        """
        catalog = lsst.afw.table.SourceCatalog(self.measurement.schema)
        catalog.getTable().setMetadata(self.measurement.algMetadata)
        datasetType = self.dataPrefix + "ForcedPhot_src"
        return {datasetType: catalog}

    def getExposure(self, dataRef):
        """!Read input exposure on which to perform the measurements
        @param dataRef Data reference from butler.
        """
        return dataRef.get(self.dataPrefix + "calexp", immediate=True)
'''
