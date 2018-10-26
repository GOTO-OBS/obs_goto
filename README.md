# An LSST Obs package for the GOTO wide-field survey

This obs package tells the LSST stack how to process data taken with the GOTO telescope. It describes:
- the basic properties of the detectors in `camera` (size, gain etc);
- the filesystem of the input and output data in `policy`;
- the configuration parameters that tell the stack's processing modules what to do in `config`;

and includes various python scripts in `python/lsst/obs_goto/` which the stack uses to interact with the data.

To use this obs package, you first need to install the LSST stack on your system. Installation instructions are provided at:
https://pipelines.lsst.io/install/lsstsw.html
I prefer to use `bash`; when I first started using the LSST stack, I tried to run it under C-shell, but it failed. I could only get it to work using bash, and I"ve stuck with that ever since.

I also recommend that you run the `lsstsw/bin/setup.sh` script each time you open a new shell by adding the command to you `.bashrc` file (the following instructions assume that you have done so).

After the install script has finished running, you must clone this repository into the stack. From within the directory you called the install script from, execute the following:
```
cd lsstsw/stack/Linux64
git clone git@github.com:GOTO-OBS/obs_goto.git
```

Next, you must tell the stack how to find `obs_goto`. This is done using the eups versioning system (which is installed as part of the stack). At the (bash) command line execute:
```
eups declare obs_goto v1 -r /full/path/to/lsstsw/stack/Linux64/
```

Once `obs_goto` has been declared, you can start to process data. In summary, the following block of bash commands will:
- ingest raw data;
- create and ingest calibration frames;
- process the exposures, including source detection;
- coadd the exposures to create a deep coadd, and perform source detection on coadd.

Assuming all your raw data is contained within `./raw_data`:
```
#!/bin/bash
mkdir -p DATA/CALIB
echo "lsst.obs.goto.gotoMapper.GotoMapper" > DATA/_mapper

ingestImages.py DATA ./rawData/*.fits --mode=link --ignore-ingested

constructBias.py DATA --calib DATA/CALIB --output=Cals --id dataType=BIAS --cores=6 --clobber-config
ingestCalibs.py DATA --calib DATA/CALIB 'Cals/BIAS/*/NONE/*.fits' --validity 180

constructDark.py DATA --calib DATA/CALIB --output=Cals --id dataType=DARK --cores=6 --clobber-config
ingestCalibs.py DATA --calib DATA/CALIB 'Cals/DARK/*/NONE/*.fits' --validity 180

constructFlat.py DATA --calib DATA/CALIB --output=Cals --id dataType=FLAT filter=G --cores=6 --clobber-config
ingestCalibs.py DATA --calib DATA/CALIB 'Cals/FLAT/*/*/*.fits' --validity 180 --config clobber=True

singleFrameDriver.py DATA --rerun outSFD --calib DATA/CALIB --id filter=G --clobber-config --cores 6
makeDiscreteSkyMap.py DATA --rerun outSFD:outMDSM --id filter=G --clobber-config
coaddDriver.py DATA --id filter=G --cores 6 --rerun outMDSM:outCD --clobber-config
multiBandDriver.py DATA --id filter=L dateObs=2018-07-22 --cores 6 --rerun outCD:outMBD --clobber-config
```

Other filters can be processed via `filter=X` within the `--id` block.  
