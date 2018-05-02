import lsst.afw.cameraGeom.cameraConfig

#This simply asserts whether the config class is of the
#right format.
assert type(config)==lsst.afw.cameraGeom.cameraConfig.CameraConfig, 'config is of type %s.%s instead of lsst.afw.cameraGeom.cameraConfig.CameraConfig' % (type(config).__module__, type(config).__name__)

#Sets the plate scale in arcsec/mm:
print ("CAMERA.PY WARNING: Platescale not set to correct value.")
config.plateScale=206.67

#This defines the native coordinate system:
#FocalPlane is (x,y) in mm (rather than radians or pixels, for example).
config.transformDict.nativeSys='FocalPlane'

#For some reason, it must have "Pupil" defined:
config.transformDict.transforms={}
config.transformDict.transforms['FieldAngle']=lsst.afw.geom.transformConfig.TransformConfig()

#I don't know what this does, but it's required to run so needs investigating.
print ("CAMERA.PY WARNING: Pupil transform currently set to 'inverted', but needs investigating.") 
#import lsst.afw.geom.xyTransformFactory
#config.transformDict.transforms[''].transform['inverted'].transform.retarget(target=lsst.afw.geom.xyTransformFactory.makeRadialXYTransform, ConfigClass=lsst.afw.geom.xyTransformFactory.RadialXYTransformConfig)
config.transformDict.transforms['FieldAngle'].transform['inverted'].transform.retarget(target=lsst.afw.geom.transformRegistry['radial'])
# Coefficients for the radial polynomial; coeff[0] must be 0
config.transformDict.transforms['FieldAngle'].transform['inverted'].transform.coeffs=[0.0, 12500.89734830887]
config.transformDict.transforms['FieldAngle'].transform.name='inverted'

#Define a list of detectors:
config.detectorList={}
config.detectorList[0]=lsst.afw.cameraGeom.cameraConfig.DetectorConfig()

#The following numbers are simply taken from SDSS:
print ("CAMERA.PY WARNING: Currently using SDSS detector values.")
#All non-commented lines ARE REQUIRED for CameraMapper:
# y0 of pixel bounding box
config.detectorList[0].bbox_y0=0
#config.detectorList[0].bbox_y0=1328

# y1 of pixel bounding box
config.detectorList[0].bbox_y1=6131
#config.detectorList[0].bbox_y1=1790

# x1 of pixel bounding box
config.detectorList[0].bbox_x1=8175
#config.detectorList[0].bbox_x1=1518

# x0 of pixel bounding box
config.detectorList[0].bbox_x0=0
#config.detectorList[0].bbox_x0=1056

# Name of detector slot
config.detectorList[0].name='g2_goto'

# Pixel size in the x dimension in mm
config.detectorList[0].pixelSize_x=0.006

# Name of native coordinate system
config.detectorList[0].transformDict.nativeSys='Pixels'

#config.detectorList[0].transformDict.transforms=None
# x position of the reference point in the detector in pixels in transposed coordinates.
config.detectorList[0].refpos_x=4087.5
#config.detectorList[0].refpos_x=1287

# y position of the reference point in the detector in pixels in transposed coordinates.
config.detectorList[0].refpos_y=3065.5
#config.detectorList[0].refpos_y=1554

# Pixel size in the y dimension in mm
config.detectorList[0].pixelSize_y=0.006

# Detector type: SCIENCE=0, FOCUS=1, GUIDER=2, WAVEFRONT=3
config.detectorList[0].detectorType=0

# x offset from the origin of the camera in mm in the transposed system.
config.detectorList[0].offset_x=158.75

# y offset from the origin of the camera in mm in the transposed system.
config.detectorList[0].offset_y=106.67999999999999

# Transpose the pixel grid before orienting in focal plane?
#config.detectorList[0].transposeDetector=False

# yaw (rotation about z) of the detector in degrees. This includes any necessary rotation to go from detector coordinates to camera coordinates after optional transposition.
config.detectorList[0].yawDeg=0.0

# roll (rotation about x) of the detector in degrees
config.detectorList[0].rollDeg=0.0

# Serial string associated with this specific detector
config.detectorList[0].serial='g2_goto'

# pitch (rotation about y) of the detector in degrees
config.detectorList[0].pitchDeg=0.0

# ID of detector slot
config.detectorList[0].id=0

# Coefficients for radial distortion
#config.radialCoeffs=None

# Name of this config
#This isn't strictly required for CameraMapper
#but I'm keeping it there as it seems like a good idea:
config.name='Goto'



