from lsst.obs.goto.forcedPhotCalexp import CosReferencesTask

for i in [
        #'base_PsfFlux',#Not needed
        'base_PeakLikelihoodFlux',#Not needed
        'base_GaussianFlux',#Not needed
        #'base_NaiveCentroid',
        'base_SdssCentroid',
        'base_SdssShape', #Not needed
        'base_ScaledApertureFlux',#Not needed
        #'base_CircularApertureFlux',
#        'base_TransformedCentroid',
        'base_Blendedness', #Not needed
        'base_LocalBackground', #Not needed
        'base_Variance', #Not needed
        'base_InputCount', #Not needed
         ]:
    config.measurement.plugins[i].doMeasure=False
    config.measurement.undeblended[i].doMeasure=False

config.measurement.plugins['base_PsfFlux'].doMeasure = True
config.measurement.undeblended['base_PsfFlux'].doMeasure = True

config.measurement.plugins['base_CircularApertureFlux'].radii=[3.0, 4.5, 6.0, 9.0, 12.0, 24.0, 48.0]
config.measurement.undeblended['base_CircularApertureFlux'].radii=[3.0, 4.5, 6.0, 9.0, 12.0, 24.0, 48.0]

# Turn off TransformedShape as it slows measurement down a lot, yet doesn't
# affect the measurement of flux. 
config.measurement.plugins.names=['base_TransformedCentroid',
                                  'base_CircularApertureFlux',
                                  'base_TransformedShape',
                                  'base_PsfFlux',
                                  ]

#Currently breaks when doing aperture corrections; fix this.
config.doApCorr=True

#CosReferencesTask causes the stack to use the COS catalogue as references,
#rather than the full reference list (since the latter takes too long).
config.references.retarget(CosReferencesTask)
config.refCat.name='deepCoadd_cos'

#Skip any tract/patch combination that does not exist.
config.references.skipMissing=True
