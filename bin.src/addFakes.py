import lsst.daf.persistence
DATA_DIR = "/local/ph1jxm/GOTO/real/DATA"
butler = lsst.daf.persistence.Butler(DATA_DIR)

exposureIdInfo = butler.get("expIdInfo", visit=15100, ccd=4, immediate=True)
import pdb
pdb.set_trace()
