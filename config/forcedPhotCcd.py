for i in [
        'base_PsfFlux',
        'base_PeakLikelihoodFlux',
        'base_GaussianFlux',
        'base_SdssShape', #base_SdssShape is needed for PSF determination.
        'base_ScaledApertureFlux',
        'base_CircularApertureFlux',
        #'base_TransformedCentroid',
        #'base_TransformedShape',
        #'base_Blendedness',
        #'base_LocalBackground',
        #'base_Variance',
        #'base_InputCount',
         ]:
    config.measurement.plugins[i].doMeasure=False
    config.measurement.undeblended[i].doMeasure=False
    
config.measurement.plugins['base_CircularApertureFlux'].radii=[6.0, 9.0, 12.0]
config.measurement.undeblended['base_CircularApertureFlux'].radii=[6.0, 9.0, 12.0]

config.measurement.plugins.names=['base_SdssCentroid',
                                  'base_TransformedCentroid',
                                  'base_CircularApertureFlux',
                                  'base_TransformedShape']

#Currently breaks when doing aperture corrections; fix this.
config.doApCorr=False
