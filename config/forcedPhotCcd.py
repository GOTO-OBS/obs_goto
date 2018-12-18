for i in [
        'base_PsfFlux',#Not needed
        'base_PeakLikelihoodFlux',#Not needed
        'base_GaussianFlux',#Not needed
        'base_NaiveCentroid',
        'base_SdssCentroid',
        'base_SdssShape', #Not needed
        'base_ScaledApertureFlux',#Not needed
        #'base_CircularApertureFlux',
#        'base_TransformedCentroid',
#        'base_TransformedShape',
        'base_Blendedness', #Not needed
        'base_LocalBackground', #Not needed
        'base_Variance', #Not needed
        'base_InputCount', #Not needed
         ]:
    config.measurement.plugins[i].doMeasure=False
    config.measurement.undeblended[i].doMeasure=False

config.measurement.plugins['base_CircularApertureFlux'].radii=[6.0, 9.0, 12.0, 24.0, 48.0]
config.measurement.undeblended['base_CircularApertureFlux'].radii=[6.0, 9.0, 12.0, 24.0, 48.0]

config.measurement.plugins.names=['base_TransformedCentroid',
                                  'base_CircularApertureFlux',
                                  'base_TransformedShape',
                                  'base_PixelFlags']

#Currently breaks when doing aperture corrections; fix this.
config.doApCorr=True

#Forced measurement currently takes about 5.5 minutes. Why is it so slow compared to normal measurement?...Because it has to warp the shapes of the apertures to match the WCS

