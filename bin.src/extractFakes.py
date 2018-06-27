import lsst.daf.persistence as dafPersistence
from astropy.io import fits
import numpy as np

DATA_DIR = "/local/ph1jxm/GOTO/real/DATA/rerun/outID"
butler = dafPersistence.Butler(DATA_DIR)

diffexp = butler.get("deepDiff_differenceExp", visit=1018021, ccd=2, immediate=True)
diasrc = butler.get("deepDiff_diaSrc", visit=1018021, ccd=2, immediate=True)
calexp = butler.get("calexp", visit=18021, ccd=2, immediate=True)

diffexpArray = diffexp.getImage().getArray()
xs,ys = diasrc.getX(), diasrc.getY()
xs,ys = xs[~np.isnan(xs)], ys[~np.isnan(ys)]


np.random.seed(1)
real_x, real_y = np.random.rand(500)*calexp.getWidth()-20, np.random.rand(500)*calexp.getHeight()+21
match = 0
i = 1
for x, y in zip(xs,ys):
    x0, y0 = int(x)-10, int(y)-10
    x1, y1 = int(x)+11, int(y)+11
    subArray = diffexpArray[y0:y1,x0:x1]
    hdu = fits.PrimaryHDU(subArray)
    dist = np.amin((real_x - x)**2 + (real_y - y)**2)
    if dist < 25:
        match += 1
        print(i,'T')
        hdu.header['REAL'] = True
    else:
        hdu.header['REAL'] = False

    filename = 'Thumbs/r1018021_%04d.fits' % i
    hdu.writeto(filename, overwrite=True)
    i+=1
    
