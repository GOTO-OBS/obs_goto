import lsst.afw.table as afwTable
import lsst.afw.geom as afwGeom
import numpy as np

#This is copying from afw/tests/testAmpInfoTable.py:
schema = afwTable.AmpInfoTable.makeMinimalSchema()
catalog = afwTable.AmpInfoCatalog(schema)
record = catalog.addNew()

name = 'Amp1'
bbox = afwGeom.Box2I(afwGeom.Point2I(0, 0), afwGeom.Extent2I(8176, 6132))
gain = 0.7
saturation = 57571
readNoise = 12.5
readoutCorner = afwTable.LL #I think this means Lower Left.
linearityCoeffs = (1.0, np.nan, np.nan, np.nan)
linearityType = "None"
rawBBox = afwGeom.Box2I(afwGeom.Point2I(0, 0), afwGeom.Extent2I(8176,6132))
rawXYOffset = afwGeom.Extent2I(0, 0)
rawDataBBox = afwGeom.Box2I(afwGeom.Point2I(0, 0), afwGeom.Extent2I(8176,6132))
#rawHorizontalOverscanBBox = afwGeom.Box2I(afwGeom.Point2I(8176, 0), afwGeom.Extent2I(0, 8176))
#rawVerticalOverscanBBox = afwGeom.Box2I(afwGeom.Point2I(6132, 0), afwGeom.Extent2I(0, 6132))
rawPrescanBBox = afwGeom.Box2I(afwGeom.Point2I(0, 0), afwGeom.Extent2I(0, 0))

record.setHasRawInfo(True) #Sets the first Flag=True
record.setRawFlipX(False)  #Sets the second Flag=False
record.setRawFlipY(False)  #Sets the third Flag=False
record.setBBox(bbox)
record.setName(name)
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
#record.setRawVerticalOverscanBBox(rawVerticalOverscanBBox)
record.setRawPrescanBBox(rawPrescanBBox)

catalog.writeFits('g1_goto.fits')
