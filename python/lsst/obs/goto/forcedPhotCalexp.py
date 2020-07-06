#!/usr/bin/env python
import lsst.afw.geom
import lsst.afw.image
from lsst.meas.base.forcedPhotCcd import ForcedPhotCcdTask, ForcedPhotCcdConfig, imageOverlapsTract
from lsst.meas.base.forcedPhotImage import ForcedPhotImageTask, ForcedPhotImageConfig

class ForcedPhotCalexpConfig(ForcedPhotCcdConfig):
    pass

class ForcedPhotCalexpTask(ForcedPhotCcdTask):
    
    ConfigClass = ForcedPhotCalexpConfig
    _DefaultName = "forcedPhotCalexp"
    dataPrefix = ""
    
    def runDataRef(self, dataRef, psfCache=None):
        """This does the same as ForcedPhotImageTask.run, but finds the
        required tract if it's not already contained in dataRef.
        """
        try:
            dataRef.dataId["tract"]
        except:
            self.getTract(dataRef)
            
        refWcs = self.references.getWcs(dataRef)
        exposure = self.getExposure(dataRef)
        if psfCache is not None:
            exposure.getPsf().setCacheSize(psfCache)
        refCat = self.fetchReferences(dataRef, exposure)
        measCat = self.measurement.generateMeasCat(exposure, refCat, refWcs,
                                                   idFactory=self.makeIdFactory(dataRef))
        self.log.info("Performing forced measurement on %s" % (dataRef.dataId,))
        self.attachFootprints(measCat, refCat, exposure, refWcs, dataRef)

        self.measurement.runDataRef(measCat, exposure, refCat, refWcs, exposureId=self.getExposureId(dataRef))

        if self.config.doApCorr:
            self.applyApCorr.run(
                catalog=measCat,
                apCorrMap=exposure.getInfo().getApCorrMap()
            )
        self.catalogCalculation.run(measCat)

        self.writeOutput(dataRef, measCat)

    def getTract(self, selectRef):

        skymap = selectRef.get("deepCoadd_skyMap")

        md = selectRef.get("calexp_md", immediate=True)
        wcs = lsst.afw.geom.makeSkyWcs(md)
        box = lsst.geom.Box2D(lsst.afw.image.bboxFromMetadata(md))
        tract = skymap.findTract(wcs.pixelToSky(box.getCenter()))
        
        if imageOverlapsTract(tract, wcs, box):
            selectRef.dataId['tract'] = tract.getId()
