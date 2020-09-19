import lsst.afw.table as afwTable
import lsst.afw.geom as afwGeom
import numpy as np

# This is copying from afw/tests/testAmpInfoTable.py:
readout = {
    'UT7':[20.9,20.6],
    'UT6':[23.0,22.1],
    'UT3':[22.1,20.7],
    'UT2':[23.0,23.4]
    }   
gain_all = {
    'UT7':[0.65,0.65],
    'UT6':[0.52,0.52],
    'UT3':[0.59,0.57],
    'UT2':[0.59,0.59]
    }

def addAmp(ampCatalog,i,rN,gain_s):
    record = ampCatalog.addNew()

    width = 4152
    height = 6220

    os = 10 #pixels of overscan
    
    bbox = afwGeom.Box2I(afwGeom.Point2I(0, 0), afwGeom.Extent2I(4088, 6132))
    bbox.shift(afwGeom.Extent2I(4088*i,0))
    
    gain = gain_s
    saturation = 65535
    readNoise = rN
    readoutCorner = afwTable.LL if i == 0 else afwTable.LR
    linearityCoeffs = (1.0, np.nan, np.nan, np.nan)
    linearityType = "None"
    rawBBox = afwGeom.Box2I(afwGeom.Point2I(0, 0), afwGeom.Extent2I(width,height))
    rawXYOffset = afwGeom.Extent2I(0, 0)
    rawDataBBox = afwGeom.Box2I(afwGeom.Point2I(64 if i==0 else 0, 44), afwGeom.Extent2I(4088,6132))
    rawHorizontalOverscanBBox = afwGeom.Box2I(afwGeom.Point2I(1 if i==0 else width-os-1, 0), afwGeom.Extent2I(os, 6220))
    #rawVerticalOverscanBBox = afwGeom.Box2I(afwGeom.Point2I(50, 6132), afwGeom.Extent2I(0, 0))
    #rawPrescanBBox = afwGeom.Box2I(afwGeom.Point2I(0, 0), afwGeom.Extent2I(0, 0))
    emptyBox = afwGeom.BoxI()

    shiftp = afwGeom.Extent2I((width)*i,0)
    rawBBox.shift(shiftp)
    rawDataBBox.shift(shiftp)
    rawHorizontalOverscanBBox.shift(shiftp)
    
    record.setHasRawInfo(True) #Sets the first Flag=True
    record.setRawFlipX(False)  #Sets the second Flag=False
    record.setRawFlipY(False)  #Sets the third Flag=False
    record.setBBox(bbox)
    record.setName('left' if i == 0 else 'right')
    record.setGain(gain)
    record.setSaturation(saturation)
    record.setReadNoise(readNoise)
    record.setReadoutCorner(readoutCorner)
    record.setLinearityCoeffs(linearityCoeffs)
    record.setLinearityType(linearityType)
    record.setRawBBox(rawBBox)
    record.setRawXYOffset(rawXYOffset)
    record.setRawDataBBox(rawDataBBox)
    record.setRawHorizontalOverscanBBox(rawHorizontalOverscanBBox)
    record.setRawVerticalOverscanBBox(emptyBox)
    record.setRawPrescanBBox(emptyBox)

def makeCcd(utId):
    schema = afwTable.AmpInfoTable.makeMinimalSchema()
    ampCatalog = afwTable.AmpInfoCatalog(schema)
    for i in range(2):
        addAmp(ampCatalog, i, readout[utId][i], gain_all[utId][i])
    return ampCatalog.writeFits('g%s_goto.fits' % utId[-1])

def main():
    uts = ['UT2','UT3','UT6','UT7']
    for ut in uts:
        camera = makeCcd(ut)

if __name__ == "__main__":
    main()
