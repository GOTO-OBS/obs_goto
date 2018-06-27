import lsst.daf.persistence as dafPersistence
import lsst.afw.image as afwImage
import lsst.afw.geom as afwGeom
import lsst.afw.display.ds9 as ds9
import numpy as np
from astropy.io import fits

DATA_DIR = "/local/ph1jxm/GOTO/real/DATA/rerun/outSF"
butler = dafPersistence.Butler(DATA_DIR)

calexp = butler.get("calexp", visit=18021, ccd=2, immediate=True)

np.random.seed(1)
nstars = 500
xs, ys = np.random.rand(nstars)*calexp.getWidth(), np.random.rand(nstars)*calexp.getHeight()  
mags = 15.+15.*np.random.rand(nstars)

srcarr = np.zeros((88+calexp.getHeight(), 128+calexp.getWidth()))

for x, y, mag in zip(xs,ys,mags):
    print('circle(%f,%f,5")'%(x,y))
    psf = calexp.getPsf().computeImage(afwGeom.Point2D(x,y)).getArray()
    flux = 120.*calexp.getCalib().getFlux(mag)
    x0, y0 = 44+int(x)-7, 64+int(y)-7
    x1, y1 = 44+int(x)+8, 64+int(y)+8
    srcarr[y0:y1,x0:x1] = srcarr[y0:y1,x0:x1] + flux*psf

hdu = fits.open("/local/ph1jxm/GOTO/real/raw/r0018021_UT2.fits")
hdu[1].data = hdu[1].data + srcarr
hdu[1].header['RUN-ID'] = 'r1018021'
#hdu.writeto("/local/ph1jxm/GOTO/real/raw/r1018021_UT2.fits", overwrite=True)


