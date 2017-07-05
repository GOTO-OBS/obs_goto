import re
import os

from lsst.daf.persistence import Policy
from lsst.obs.base import CameraMapper, exposureFromImage
import lsst.afw.image.utils as afwImageUtils
import lsst.afw.image as afwImage
from lsst.ip.isr import IsrTask
from .makeGotoRawVisitInfo import MakeGotoRawVisitInfo

class GotoMapper(CameraMapper):
    packageName = 'obs_goto'

    MakeRawVisitInfoClass = MakeGotoRawVisitInfo
    
    def __init__(self, inputPolicy=None, **kwargs):

        #Define the policy file:
        policyFile = Policy.defaultPolicyFile(self.packageName, "GotoMapper.yaml", "policy")
        policy =Policy(policyFile)
        
        #This creates the camera class by calling CameraMapper (i.e., the parent class):
        
        super(GotoMapper, self).__init__(policy, os.path.dirname(policyFile), **kwargs)
        
        #Set the filters:
        self.filterIdMap = dict(v=0)
        afwImageUtils.defineFilter(name='v',  lambdaEff=450, alias=['v'])
        afwImageUtils.defineFilter(name='m',  lambdaEff=610.5, alias=['m'])
        afwImageUtils.defineFilter(name='Clear',  lambdaEff=450, alias=['Clear'])

        self.filters = {}
        self.filters['v'] = afwImage.Filter('v').getCanonicalName()
        self.filters['m'] = afwImage.Filter('m').getCanonicalName()
        self.filters['Clear'] = afwImage.Filter('Clear').getCanonicalName()
        
        self.defaultFilterName = 'm'
        
        
    
    def _computeCcdExposureId(self, dataId):
        """Compute the 64-bit (long) identifier for a CCD exposure.
        @param dataId (dict) Data identifier with visit and CCD
        """
        #This can change for the real GOTO data/header. What combination will make a CCD exposure unique?
        pathId = self._transformId(dataId)
        visit = pathId['visit']
        ccd = pathId['ccd']
        visit = int(visit)
        ccd = int(ccd)
        
        return visit*10+ccd
        
    
    def bypass_ccdExposureId(self, datasetType, pythonType, location, dataId):
        
        return self._computeCcdExposureId(dataId)

    def bypass_ccdExposureId_bits(self, datasetType, pythonType, location, dataId):
        
        return 42
       

#    def _extractDetectorName(self, dataId):

#    def _standardizeExposure(self, mapping, item, dataId, filter=True,
#                             trimmed=True):
#        """Default standardization function for images.
#        @param mapping (lsst.daf.butlerUtils.Mapping)
#        @param[in,out] item (lsst.afw.image.Exposure)
#        @param dataId (dict) Dataset identifier
#        @param filter (bool) Set filter?
#        @param trimmed (bool) Should detector be marked as trimmed?
#        @return (lsst.afw.image.Exposure) the standardized Exposure"""
#        return item

    def standardizeCalib(self, dataset, item, dataId):

        mapping = self.calibrations[dataset]
        if "Image" in mapping.python:
            exp = afwImage.makeMaskedImage(item)
        exp = afwImage.makeExposure(exp)    
        exp = self._standardizeExposure(mapping, exp, \
                                        dataId, filter=False, trimmed=False)        
        return exp

    def std_bias(self, item, dataId):
        return self.standardizeCalib("bias", item, dataId)

    def std_dark(self, item, dataId):
        exp = self._standardizeExposure(self.calibrations['dark'], \
                                        item, dataId, trimmed=False, filter=False)
        visitInfo = afwImage.makeVisitInfo(exposureTime=1.0, darkTime=1.0)
        exp.getInfo().setVisitInfo(visitInfo)
        return exp
                            
    def std_flat(self, item, dataId):
        return self.standardizeCalib("flat", item, dataId)

    def std_raw(self, item, dataId):
        raw = super(GotoMapper, self).std_raw(item, dataId)
        
        return raw 
                                        
    def bypass_Mask(self, datasetType, pythonType, location, dataID):
        print "bypass_Mask"
        return convertmask(location.getLocations()[0])
    
    def bypass_WCS(self, datasetType, pythonType, location, dataId):
        print "bypass_WCS"
        return convertWCS(location.getLocations()[0])


    def bypass_deepCoaddId_bits(self, *args, **kwargs):
        return 32

    def bypass_deepCoaddId(self, datasetType, pythonType, location, dataId):
        return 32

    def bypass_deepMergedCoaddId_bits(self, *args, **kwargs):
        """The number of bits used up for patch ID bits"""
        return 32

    def bypass_deepMergedCoaddId(self, datasetType, pythonType, location, dataId):
        return 32
  
    def bypass_tsField(self, datasetType, pythonType, location, dataId):
        print 'tsField Location', location.getLocations()[0]
        return 50, 50

    def _extractDetectorName(self, dataId):
        return "g1_goto"
    
