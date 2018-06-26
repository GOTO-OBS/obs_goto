import lsst.daf.persistence as dafPersistence
import lsst.afw.image as afwImage
import lsst.afw.geom as afwGeom
import lsst.afw.display.ds9 as ds9
import numpy as np

DATA_DIR = "/local/ph1jxm/GOTO/real/DATA/rerun/outSF"
butler = dafPersistence.Butler(DATA_DIR)

calexp = butler.get("calexp", visit=18021, ccd=2, immediate=True)
psf = calexp.getPsf().computeImage(afwGeom.Point2D(10,10))

srcarr = np.zeros((calexp.getHeight(), calexp.getWidth()))

postISR = butler.get("postISRCCD", visit=18021, ccd=2, immediate=True)


import pdb
pdb.set_trace()
