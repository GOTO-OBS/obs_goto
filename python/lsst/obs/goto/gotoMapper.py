from __future__ import absolute_import, division, print_function

import re
import os


from lsst.daf.persistence import Policy
from lsst.obs.base import CameraMapper, exposureFromImage
import lsst.afw.image.utils as afwImageUtils
import lsst.afw.image as afwImage
import lsst.afw.geom as afwGeom
from lsst.ip.isr import IsrTask
from .makeGotoRawVisitInfo import MakeGotoRawVisitInfo
from astropy import coordinates, units 


class GotoMapper(CameraMapper):
    packageName = 'obs_goto'

    MakeRawVisitInfoClass = MakeGotoRawVisitInfo
    
    def __init__(self, inputPolicy=None, **kwargs):

        #Define the policy file:
        policyFile = Policy.defaultPolicyFile(self.packageName, "GotoMapper.yaml", "policy")
        policy =Policy(policyFile)
        
        #This creates the camera class by calling CameraMapper (i.e., the parent class):
        super(GotoMapper, self).__init__(policy, os.path.dirname(policyFile), **kwargs)

        # Ensure each dataset type of interest knows about the full range of keys available from the registry
        keys = {'visit': int,
                'ccd': int,
                'filter': str,
                'dataType': str,
                'expTime': float,
                'dateObs': str,
                'taiObs': str,
                'mjd': int,
                'field': str,
                'survey': str}
        for name in ("raw",
                     "postISRCCD", "calexp", "src", "icSrc", "srcMatch",
                    ):
            self.mappings[name].keyDict.update(keys)
        
        #Set the filters:
        self.filterIdMap = dict(v=0)
        afwImageUtils.defineFilter(name='R',  lambdaEff=635.9, alias=['R'])
        afwImageUtils.defineFilter(name='G',  lambdaEff=534.9, alias=['G'])
        afwImageUtils.defineFilter(name='B',  lambdaEff=446.6, alias=['B'])
        afwImageUtils.defineFilter(name='L',  lambdaEff=535.5, alias=['L'])
        
        self.filters = {}
        self.filters['R'] = afwImage.Filter('R').getCanonicalName()
        self.filters['G'] = afwImage.Filter('G').getCanonicalName()
        self.filters['B'] = afwImage.Filter('B').getCanonicalName()
        self.filters['L'] = afwImage.Filter('L').getCanonicalName()
        self.defaultFilterName = 'L'
    
    def _computeCcdExposureId(self, dataId):
        """Compute the 64-bit identifier for a CCD exposure.
        @param dataId (dict) Data identifier with visit and CCD
        
        We uniquely identify an exposure via its visit ID (i.e., r******) and its ccd (UT number).

        We allow for up to 2**24 = 16,777,216 visits, and up to 2**6 = 64 UTs
        The first 34 (right to left) bits give the object ID (overkill).
        The next 6 give the UT.
        The next 24 give the visit number.

        If you want to add a filter code (up to 2**3 = 8 filters, say):
        return visit*64*8 + filt*64 + ccd
        Then add 3 to the 30 in bypass_ccdExposureId_bits

        """
        
        pathId = self._transformId(dataId)
        visit = pathId['visit']
        ccd = pathId['ccd']
        visit = int(visit)
        ccd = int(ccd)

        return visit*64 + ccd

    def bypass_ccdExposureId(self, datasetType, pythonType, location, dataId):
        
        return self._computeCcdExposureId(dataId)

    def bypass_ccdExposureId_bits(self, datasetType, pythonType, location, dataId):
        return 24+6

    def _computeCoaddExposureId(self, dataId):
        '''
        Here I'm saying: 
           - we've got up to 1024 (2**10) tracts;
           - we've got up to 64 (2**6) patches in each dimension
        Currently, I'm not incorporating filter information.
        The remaining 64-22 = 42 bits are left for source numbers
        '''
        nbit_tract = 10
        nbit_patch = 6
        tract = int(dataId['tract'])

        patchX, patchY = [int(patch) for patch in dataId['patch'].split(',')]
        oid = (((tract << nbit_patch) + patchX) << nbit_patch) + patchY
        
        return oid

    def bypass_deepCoaddId_bits(self, *args, **kwargs):
        #Up to 1024 (2**10) tracts each containing up to 64x64 (2**6x2**6) patches
        return 10+6+6 

    def bypass_deepCoaddId(self, datasetType, pythonType, location, dataId):
        return self._computeCoaddExposureId(dataId)

    def bypass_deepMergedCoaddId_bits(self, *args, **kwargs):
         return 10+6+6

    def bypass_deepMergedCoaddId(self, datasetType, pythonType, location, dataId):
        return self._computeCoaddExposureId(dataId)

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

        #This creates an approximate wcs based on RA-TEL and DEC-TEL.
        raw = super(GotoMapper, self).std_raw(item, dataId)
        md = raw.getMetadata()        

        ra_deg = (coordinates.Angle(md.get('RA-TEL'), unit=units.hour).deg)
        de_deg = (coordinates.Angle(md.get('DEC-TEL'), unit=units.deg).deg)

        md.setDouble("CRVAL1", ra_deg)
        md.setDouble("CRVAL2", de_deg)
        md.setDouble("CRPIX1", 0.)
        md.setDouble("CRPIX2", 0.)
        md.setDouble('CDELT1',1.0)
        md.setDouble('CDELT2',1.0)
        md.set("CUNIT1",'deg')
        md.set("CUNIT2",'deg')
        
        md.setDouble("CD1_1", 1.0E-6)
        md.setDouble("CD1_2", -3.4E-04)
        md.setDouble("CD2_1", 3.4E-04)
        md.setDouble("CD2_2", 1.0E-6)

        md.set("CTYPE1", 'RA---TAN-SIP')
        md.set("CTYPE2", 'DEC--TAN-SIP')
        
        wcs = afwGeom.makeSkyWcs(md)
        raw.setWcs(wcs)
        
        return raw 
                                        
    def bypass_Mask(self, datasetType, pythonType, location, dataID):
        print ("bypass_Mask")
        return convertmask(location.getLocations()[0])
    
    def bypass_tsField(self, datasetType, pythonType, location, dataId):
        #print 'tsField Location', location.getLocations()[0]
        return 50, 50

    def _extractDetectorName(self, dataId):
        return int("%(ccd)d" % dataId)
    
class GotoSimMapper(GotoMapper):

    def __init__(self, **kwargs):

        #Define the policy file:
        policyFile = Policy.defaultPolicyFile(self.packageName, "GotoMapper.yaml", "policy")
        policy =Policy(policyFile)

        #Change the policy to point to the sim camera description:
        policy["camera"] = "../sim/camera"
        
        #This creates the camera class by calling CameraMapper (i.e., the parent class):
        super(GotoMapper, self).__init__(policy, os.path.dirname(policyFile), **kwargs)

        #Set the filters:
        self.filterIdMap = dict(v=0)
        afwImageUtils.defineFilter(name='R',  lambdaEff=635.9, alias=['R'])
        afwImageUtils.defineFilter(name='G',  lambdaEff=534.9, alias=['G'])
        afwImageUtils.defineFilter(name='B',  lambdaEff=446.6, alias=['B'])
        afwImageUtils.defineFilter(name='L',  lambdaEff=535.5, alias=['L'])
        
        self.filters = {}
        self.filters['R'] = afwImage.Filter('R').getCanonicalName()
        self.filters['G'] = afwImage.Filter('G').getCanonicalName()
        self.filters['B'] = afwImage.Filter('B').getCanonicalName()
        self.filters['L'] = afwImage.Filter('L').getCanonicalName()
        self.defaultFilterName = 'L'
        
    @classmethod
    def getCameraName(cls):
        return "sim"
