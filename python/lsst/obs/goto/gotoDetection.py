from lsst.meas.algorithms.detection import (SourceDetectionTask, 
                                            SourceDetectionConfig)
import lsst.pex.config as pexConfig
import lsst.afw.math as afwMath
import lsst.afw.image as afwImage
import lsst.pipe.base as pipeBase

class GotoSourceDetectionConfig(SourceDetectionConfig):
    """!Configuration parameters for the GotoSourceDetectionTask
    """
    scaleSigma = pexConfig.RangeField(
        doc="Scale to multiply PSF sigma by.",
        dtype=float, optional=False, default=1.0, min=0.0,
    )

class GotoSourceDetectionTask(SourceDetectionTask):

    ConfigClass = GotoSourceDetectionConfig
    _DefaultName = "gotoSourceDetection"

    def convolveImage(self, maskedImage, psf, doSmooth=True):
            """Convolve the image with the PSF

            This differs from the standard SourceDetectionTask convolveImage
            in that it allows the user to specify a scaling to the sigma. For GOTO coadds, we found that convolving by the sigma blurred the image too much, meaning that some peaks were missed. By reducing the width of the Gaussian kernel, the smoothing is reduced.

            Parameters
            ----------
            maskedImage : `lsst.afw.image.MaskedImage`
                Image to convolve.
            psf : `lsst.afw.detection.Psf`
                PSF to convolve with (actually with a Gaussian approximation
                to it).
            doSmooth : `bool`
                Actually do the convolution?

            Return Struct contents
            ----------------------
            middle : `lsst.afw.image.MaskedImage`
                Convolved image, without the edges.
            sigma : `float`
                Gaussian sigma used for the convolution.
            """
            self.metadata.set("doSmooth", doSmooth)
            sigma = psf.computeShape().getDeterminantRadius()
            
            # This is the only thing that differs from SourceDetectionTask: 
            sigma *= self.config.scaleSigma 
            self.metadata.set("sigma", sigma)

            if not doSmooth:
                middle = maskedImage.Factory(maskedImage)
                return pipeBase.Struct(middle=middle, sigma=sigma)

            # Smooth using a Gaussian (which is separable, hence fast) of width sigma
            # Make a SingleGaussian (separable) kernel with the 'sigma'
            kWidth = self.calculateKernelSize(sigma)
            self.metadata.set("smoothingKernelWidth", kWidth)
            gaussFunc = afwMath.GaussianFunction1D(sigma)
            gaussKernel = afwMath.SeparableKernel(kWidth, kWidth, gaussFunc, gaussFunc)

            convolvedImage = maskedImage.Factory(maskedImage.getBBox())

            afwMath.convolve(convolvedImage, maskedImage, gaussKernel, afwMath.ConvolutionControl())
            #
            # Only search psf-smoothed part of frame
            #
            goodBBox = gaussKernel.shrinkBBox(convolvedImage.getBBox())
            middle = convolvedImage.Factory(convolvedImage, goodBBox, afwImage.PARENT, False)
            #
            # Mark the parts of the image outside goodBBox as EDGE

            self.setEdgeBits(maskedImage, goodBBox, maskedImage.getMask().getPlaneBitMask("EDGE"))

            return pipeBase.Struct(middle=middle, sigma=sigma)