from lsst.obs.base.ingest import RawFileData
import lsst.obs.base
from ._instrument import North1, North2

class GotoRawIngestTask(lsst.obs.base.RawIngestTask):

    def extractMetadata(self, filename: str) -> RawFileData:
        datasets = []
        fitsData = lsst.afw.fits.Fits(filename.ospath, 'r')
        fitsData.setHdu(1)
        header = fitsData.readMetadata()
        datasets.append(self._calculate_dataset_info(header, filename))
        instrument = NeCam()
        FormatterClass = instrument.getRawFormatter(datasets[0].dataId)

        return RawFileData(datasets=datasets, filename=filename,
                           FormatterClass=FormatterClass,
                           instrument=instrument)
