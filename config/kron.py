from __future__ import absolute_import, division, print_function
# Enable Kron mags
# 'config' is a SourceMeasurementConfig

try:
    import lsst.meas.extensions.photometryKron
    config.plugins.names |= ["ext_photometryKron_KronFlux"]
except ImportError:
    print ("Cannot import lsst.meas.extensions.photometryKron: disabling Kron measurements")
