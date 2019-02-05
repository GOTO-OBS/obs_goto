from collections import namedtuple
from lsst.pipe.tasks.fakes import BaseFakeSourcesConfig, BaseFakeSourcesTask
import lsst.afw.geom as afwGeom
import numpy as np

positionTuple = namedtuple("positionTuple", "y x")


class FakeSourcesTestConfig(BaseFakeSourcesConfig):
    pass


class FakeSourcesTestTask(BaseFakeSourcesTask):
    '''
    A task to insert fake objects into test data to verify the hooks for the
    fake object pipeline work.
    '''

    ConfigClass = FakeSourcesTestConfig
    _DefaultName = "fakeSourcesTest"

    # Ground truth position and intensities for the fake sources
    fakeSources = [(positionTuple(800, 435), 11342),
                   (positionTuple(400, 350), 18235),
                   (positionTuple(1834, 379), 13574),
                   (positionTuple(1234, 642), 12456)]
    def __init__(self, **kwargs):
        BaseFakeSourcesTask.__init__(self, **kwargs)

    def run(self, exposure, background):
        if not exposure.hasPsf():
            raise RuntimeError("Exposure object must have a PSF")
        # Fetch objects from the exposure
        psf = exposure.getPsf()
        image = exposure.getMaskedImage().getImage()
        mask = exposure.getMaskedImage().getMask()
        variance = exposure.getMaskedImage().getVariance()

        y0 = image.getY0()
        x0 = image.getX0()

        # Bitplane to set corresponding to the FAKE bit
        fakeMaskValue = 2**mask.getMaskPlaneDict()['FAKE']

        # At each position create a star with the given intensity and add it
        # to the image.
        for pos, intensity in self.fakeSources:
            objArray, noiseArray = self.makeFakeStar(pos, intensity, psf)
            psfRad = int((objArray.shape[0]-1)/2.)
            yslice, xslice = slice(pos.y-psfRad-y0, pos.y+psfRad+y0+1),\
                slice(pos.x-psfRad-x0, pos.x+psfRad+x0+1)

            image.getArray()[yslice, xslice] += objArray
            mask.getArray()[yslice, xslice] += fakeMaskValue
            variance.getArray()[yslice, xslice] += noiseArray**2

    # make stars at a given position with a given intensity
    @staticmethod
    def makeFakeStar(position, intensity, psf):
        psfImage = psf.computeImage(afwGeom.Point2D(position.x, position.y)).getArray()
        psfImage *= intensity
        noise = np.random.normal(0, np.sqrt(abs(psfImage)))
        return psfImage + noise, noise    
