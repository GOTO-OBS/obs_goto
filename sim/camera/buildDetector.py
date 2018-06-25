import lsst.afw.table as afwTable
import lsst.afw.geom as afwGeom
import numpy as np

# This is copying from afw/tests/testAmpInfoTable.py:
def addAmp(ampCatalog):
    record = ampCatalog.addNew()

    width = 4301
    height = 4551

    os = 0 #pixels of overscan
    
    bbox = afwGeom.Box2I(afwGeom.Point2I(0, 0), afwGeom.Extent2I(4301, 4551))
    
    gain = 0.7
    saturation = 65535
    readNoise = 12.5
    readoutCorner = afwTable.LL
    linearityCoeffs = (1.0, np.nan, np.nan, np.nan)
    linearityType = "None"
    rawBBox = afwGeom.Box2I(afwGeom.Point2I(0, 0), afwGeom.Extent2I(width,height))
    rawXYOffset = afwGeom.Extent2I(0, 0)
    rawDataBBox = afwGeom.Box2I(afwGeom.Point2I(0, 0), afwGeom.Extent2I(4301,4551))
    #rawHorizontalOverscanBBox = afwGeom.Box2I(afwGeom.Point2I(0 if i==0 else width-os, 0), afwGeom.Extent2I(os, 6220))
    #rawVerticalOverscanBBox = afwGeom.Box2I(afwGeom.Point2I(50, 6132), afwGeom.Extent2I(0, 0))
    #rawPrescanBBox = afwGeom.Box2I(afwGeom.Point2I(0, 0), afwGeom.Extent2I(0, 0))
    emptyBox = afwGeom.BoxI()

    #shiftp = afwGeom.Extent2I(0,0)
    #rawBBox.shift(shiftp)
    #rawDataBBox.shift(shiftp)
    #rawHorizontalOverscanBBox.shift(shiftp)
    
    record.setHasRawInfo(True) #Sets the first Flag=True
    record.setRawFlipX(False)  #Sets the second Flag=False
    record.setRawFlipY(False)  #Sets the third Flag=False
    record.setBBox(bbox)
    record.setName('left')
    record.setGain(gain)
    record.setSaturation(saturation)
    record.setReadNoise(readNoise)
    record.setReadoutCorner(readoutCorner)
    record.setLinearityCoeffs(linearityCoeffs)
    record.setLinearityType(linearityType)
    record.setRawBBox(rawBBox)
    record.setRawXYOffset(rawXYOffset)
    record.setRawDataBBox(rawDataBBox)
    #record.setRawHorizontalOverscanBBox(rawHorizontalOverscanBBox)
    record.setRawVerticalOverscanBBox(emptyBox)
    record.setRawPrescanBBox(emptyBox)

def makeCcd():
    schema = afwTable.AmpInfoTable.makeMinimalSchema()
    ampCatalog = afwTable.AmpInfoCatalog(schema)

    addAmp(ampCatalog)
    
    return ampCatalog.writeFits('g2_goto.fits')

def main():
    camera = makeCcd()

if __name__ == "__main__":
    main()
