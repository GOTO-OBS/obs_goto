#
# LSST Data Management System
# Copyright 2008-2016 AURA/LSST.
#
# This product includes software developed by the
# LSST Project (http://www.lsst.org/).
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the LSST License Statement and
# the GNU General Public License along with this program.  If not,
# see <https://www.lsstcorp.org/LegalNotices/>.
#
# @package lsst.pipe.tasks.
import sys
import numpy as np
import lsst.pipe.base as pipeBase
from lsst.pipe.tasks.photoCal import PhotoCalTask, PhotoCalConfig

#__all__ = ["PhotoCalTask", "PhotoCalConfig"]

class GotoPhotoCalTask(PhotoCalTask):

    def getZeroPoint(self, src, ref, srcErr=None, zp0=None):
        """!Flux calibration code, returning (ZeroPoint, Distribution Width, Number of stars)

        We perform nIter iterations of a simple sigma-clipping algorithm with a couple of twists:
        1.  We use the median/interquartile range to estimate the position to clip around, and the
        "sigma" to use.
        2.  We never allow sigma to go _above_ a critical value sigmaMax --- if we do, a sufficiently
        large estimate will prevent the clipping from ever taking effect.
        3.  Rather than start with the median we start with a crude mode.  This means that a set of magnitude
        residuals with a tight core and asymmetrical outliers will start in the core.  We use the width of
        this core to set our maximum sigma (see 2.)

        @return Struct of:
         - zp ---------- Photometric zero point (mag)
         - sigma ------- Standard deviation of fit of zero point (mag)
         - ngood ------- Number of sources used to fit zero point
        """
        sigmaMax = self.config.sigmaMax

        dmag = ref - src

        indArr = np.argsort(dmag)
        dmag = dmag[indArr]

        if srcErr is not None:
            dmagErr = srcErr[indArr]
        else:
            dmagErr = np.ones(len(dmag))

        # need to remove nan elements to avoid errors in stats calculation with numpy
        ind_noNan = np.array([i for i in range(len(dmag))
                              if (not np.isnan(dmag[i]) and not np.isnan(dmagErr[i]))])
        dmag = dmag[ind_noNan]
        dmagErr = dmagErr[ind_noNan]

        IQ_TO_STDEV = 0.741301109252802    # 1 sigma in units of interquartile (assume Gaussian)

        npt = len(dmag)
        ngood = npt
        good = None  # set at end of first iteration
        for i in range(self.config.nIter):
            if i > 0:
                npt = sum(good)

            center = None
            if i == 0:
                #
                # Start by finding the mode
                #
                nhist = 20
                try:
                    hist, edges = np.histogram(dmag, nhist, new=True)
                except TypeError:
                    hist, edges = np.histogram(dmag, nhist)  # they removed new=True around numpy 1.5
                imode = np.arange(nhist)[np.where(hist == hist.max())]

                if imode[-1] - imode[0] + 1 == len(imode):  # Multiple modes, but all contiguous
                    if zp0:
                        center = zp0
                    else:
                        center = 0.5*(edges[imode[0]] + edges[imode[-1] + 1])

                    peak = sum(hist[imode])/len(imode)  # peak height

                    # Estimate FWHM of mode
                    j = imode[0]
                    while j >= 0 and hist[j] > 0.5*peak:
                        j -= 1
                    j = max(j, 0)
                    q1 = dmag[sum(hist[range(j)])]

                    j = imode[-1]
                    while j < nhist and hist[j] > 0.5*peak:
                        j += 1
                    j = min(j, nhist - 1)
                    j = min(sum(hist[range(j)]), npt - 1)
                    q3 = dmag[j]

                    if q1 == q3:
                        q1 = dmag[int(0.25*npt)]
                        q3 = dmag[int(0.75*npt)]

                    sig = (q3 - q1)/2.3  # estimate of standard deviation (based on FWHM; 2.358 for Gaussian)

                    if sigmaMax is None:
                        sigmaMax = 2*sig   # upper bound on st. dev. for clipping. multiplier is a heuristic

                    self.log.debug("Photo calibration histogram: center = %.2f, sig = %.2f", center, sig)

                else:
                    if sigmaMax is None:
                        sigmaMax = dmag[-1] - dmag[0]

                    center = np.median(dmag)
                    q1 = dmag[int(0.25*npt)]
                    q3 = dmag[int(0.75*npt)]
                    sig = (q3 - q1)/2.3  # estimate of standard deviation (based on FWHM; 2.358 for Gaussian)

            if center is None:              # usually equivalent to (i > 0)
                gdmag = dmag[good]
                if self.config.useMedian:
                    center = np.median(gdmag)
                else:
                    gdmagErr = dmagErr[good]
                    center = np.average(gdmag, weights=gdmagErr)

                q3 = gdmag[min(int(0.75*npt + 0.5), npt - 1)]
                q1 = gdmag[min(int(0.25*npt + 0.5), npt - 1)]

                sig = IQ_TO_STDEV*(q3 - q1)     # estimate of standard deviation

            good = abs(dmag - center) < self.config.nSigma*min(sig, sigmaMax)  # don't clip too softly

            # =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
            if self.scatterPlot:
                try:
                    self.fig.clf()

                    axes = self.fig.add_axes((0.1, 0.1, 0.85, 0.80))

                    axes.plot(ref[good], dmag[good] - center, "b+")
                    axes.errorbar(ref[good], dmag[good] - center, yerr=dmagErr[good],
                                  linestyle='', color='b')

                    bad = np.logical_not(good)
                    if len(ref[bad]) > 0:
                        axes.plot(ref[bad], dmag[bad] - center, "r+")
                        axes.errorbar(ref[bad], dmag[bad] - center, yerr=dmagErr[bad],
                                      linestyle='', color='r')

                    axes.plot((-100, 100), (0, 0), "g-")
                    for x in (-1, 1):
                        axes.plot((-100, 100), x*0.05*np.ones(2), "g--")

                    axes.set_ylim(-1.1, 1.1)
                    axes.set_xlim(24, 13)
                    axes.set_xlabel("Reference")
                    axes.set_ylabel("Reference - Instrumental")

                    self.fig.show()

                    if self.scatterPlot > 1:
                        reply = None
                        while i == 0 or reply != "c":
                            try:
                                reply = input("Next iteration? [ynhpc] ")
                            except EOFError:
                                reply = "n"

                            if reply == "h":
                                print("Options: c[ontinue] h[elp] n[o] p[db] y[es]", file=sys.stderr)
                                continue

                            if reply in ("", "c", "n", "p", "y"):
                                break
                            else:
                                print("Unrecognised response: %s" % reply, file=sys.stderr)

                        if reply == "n":
                            break
                        elif reply == "p":
                            import pdb
                            pdb.set_trace()
                except Exception as e:
                    print("Error plotting in PhotoCal.getZeroPoint: %s" % e, file=sys.stderr)

            # =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-

            old_ngood = ngood
            ngood = sum(good)
            if ngood == 0:
                msg = "PhotoCal.getZeroPoint: no good stars remain"

                if i == 0:                  # failed the first time round -- probably all fell in one bin
                    center = np.average(dmag, weights=dmagErr)
                    msg += " on first iteration; using average of all calibration stars"

                self.log.warn(msg)

                return pipeBase.Struct(
                    zp=center,
                    sigma=sig,
                    ngood=len(dmag))
            elif ngood == old_ngood:
                break

            if False:
                ref = ref[good]
                dmag = dmag[good]
                dmagErr = dmagErr[good]

        dmag = dmag[good]
        dmagErr = dmagErr[good]
        zp, weightSum = np.average(dmag, weights=1/dmagErr**2, returned=True)
        sigma = np.sqrt(1.0/weightSum)
        return pipeBase.Struct(
            zp=zp,
            sigma=sig,
            ngood=len(dmag),
        )
