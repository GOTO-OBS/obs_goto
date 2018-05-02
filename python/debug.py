import lsstDebug
def DebugInfo(name):
    di = lsstDebug.getInfo(name)        # N.b. lsstDebug.Info(name) would call us recursively
    if name == "lsst.pipe.tasks.measurePsf" :
        di.display = True
        di.displayExposure = True          # display the Exposure + spatialCells
        di.displayPsfCandidates = False      # show mosaic of candidates
        di.displayPsfMosaic = False          # show mosaic of reconstructed PSF(xy)
        di.displayResiduals = False          # show residuals
        di.showBadCandidates = False         # Include bad candidates
        di.normalizeResiduals = False       # Normalise residuals by object amplitude
    return di
lsstDebug.Info = DebugInfo
