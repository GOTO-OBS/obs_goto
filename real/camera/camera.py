import lsst.afw.cameraGeom.cameraConfig

#This simply asserts whether the config class is of the
#right format.
assert type(config)==lsst.afw.cameraGeom.cameraConfig.CameraConfig, 'config is of type %s.%s instead of lsst.afw.cameraGeom.cameraConfig.CameraConfig' % (type(config).__module__, type(config).__name__)

#Sets the plate scale in arcsec/mm:
config.plateScale=206.67

#This defines the native coordinate system:
#FocalPlane is (x,y) in mm (rather than radians or pixels, for example).
config.transformDict.nativeSys='FocalPlane'

#For some reason, it must have "Pupil" defined:
config.transformDict.transforms={}
config.transformDict.transforms['FieldAngle']=lsst.afw.geom.transformConfig.TransformConfig()

# coeffs = [0,1] is the default. This is only necessary if you want to convert
#between positions on the focal plane.
config.transformDict.transforms['FieldAngle'].transform['inverted'].transform.retarget(target=lsst.afw.geom.transformRegistry['radial'])
config.transformDict.transforms['FieldAngle'].transform['inverted'].transform.coeffs=[0.0, 1.0]
config.transformDict.transforms['FieldAngle'].transform.name='inverted'

#Define a list of detectors:
config.detectorList={}
config.detectorList[0]=lsst.afw.cameraGeom.cameraConfig.DetectorConfig()

#All non-commented lines ARE REQUIRED for CameraMapper:
# y0 of pixel bounding box
config.detectorList[0].bbox_y0=0

# y1 of pixel bounding box
config.detectorList[0].bbox_y1=6131

# x1 of pixel bounding box
config.detectorList[0].bbox_x1=8175

# x0 of pixel bounding box
config.detectorList[0].bbox_x0=0

# Name of detector slot
config.detectorList[0].name='g0_goto'

# Pixel size in mm
config.detectorList[0].pixelSize_x=0.006
config.detectorList[0].pixelSize_y=0.006

# Name of native coordinate system
config.detectorList[0].transformDict.nativeSys='Pixels'

# x position of the reference point in the detector in pixels in transposed coordinates.
config.detectorList[0].refpos_x=4087.5

# y position of the reference point in the detector in pixels in transposed coordinates.
config.detectorList[0].refpos_y=3065.5

# Detector type: SCIENCE=0, FOCUS=1, GUIDER=2, WAVEFRONT=3
config.detectorList[0].detectorType=0

# x offset from the origin of the camera in mm in the transposed system.
config.detectorList[0].offset_x=0.

# y offset from the origin of the camera in mm in the transposed system.
config.detectorList[0].offset_y=0.

config.detectorList[0].yawDeg=0.0
config.detectorList[0].rollDeg=0.0
config.detectorList[0].pitchDeg=0.0

# Serial string associated with this specific detector
config.detectorList[0].serial='1'

# ID of detector slot
config.detectorList[0].id=1


config.detectorList[1]=lsst.afw.cameraGeom.cameraConfig.DetectorConfig()

#All non-commented lines ARE REQUIRED for CameraMapper:
# y0 of pixel bounding box
config.detectorList[1].bbox_y0=0

# y1 of pixel bounding box
config.detectorList[1].bbox_y1=6131

# x1 of pixel bounding box
config.detectorList[1].bbox_x1=8175

# x0 of pixel bounding box
config.detectorList[1].bbox_x0=0

# Name of detector slot
config.detectorList[1].name='g1_goto'

# Pixel size in mm
config.detectorList[1].pixelSize_x=0.006
config.detectorList[1].pixelSize_y=0.006

# Name of native coordinate system
config.detectorList[1].transformDict.nativeSys='Pixels'

# x position of the reference point in the detector in pixels in transposed coordinates.
config.detectorList[1].refpos_x=4087.5

# y position of the reference point in the detector in pixels in transposed coordinates.
config.detectorList[1].refpos_y=3065.5

# Detector type: SCIENCE=0, FOCUS=1, GUIDER=2, WAVEFRONT=3
config.detectorList[1].detectorType=0

# x offset from the origin of the camera in mm in the transposed system.
config.detectorList[1].offset_x=0.

# y offset from the origin of the camera in mm in the transposed system.
config.detectorList[1].offset_y=0.

config.detectorList[1].yawDeg=0.0
config.detectorList[1].rollDeg=0.0
config.detectorList[1].pitchDeg=0.0

# Serial string associated with this specific detector
config.detectorList[1].serial='2'

# ID of detector slot
config.detectorList[1].id=2


config.detectorList[4]=lsst.afw.cameraGeom.cameraConfig.DetectorConfig()

#All non-commented lines ARE REQUIRED for CameraMapper:
# y0 of pixel bounding box
config.detectorList[4].bbox_y0=0

# y1 of pixel bounding box
config.detectorList[4].bbox_y1=6131

# x1 of pixel bounding box
config.detectorList[4].bbox_x1=8175

# x0 of pixel bounding box
config.detectorList[4].bbox_x0=0

# Name of detector slot
config.detectorList[4].name='g2_goto'

# Pixel size in mm
config.detectorList[4].pixelSize_x=0.006
config.detectorList[4].pixelSize_y=0.006

# Name of native coordinate system
config.detectorList[4].transformDict.nativeSys='Pixels'

# x position of the reference point in the detector in pixels in transposed coordinates.
config.detectorList[4].refpos_x=4087.5

# y position of the reference point in the detector in pixels in transposed coordinates.
config.detectorList[4].refpos_y=3065.5

# Detector type: SCIENCE=0, FOCUS=1, GUIDER=2, WAVEFRONT=3
config.detectorList[4].detectorType=0

# x offset from the origin of the camera in mm in the transposed system.
config.detectorList[4].offset_x=0.

# y offset from the origin of the camera in mm in the transposed system.
config.detectorList[4].offset_y=0.

config.detectorList[4].yawDeg=0.0
config.detectorList[4].rollDeg=0.0
config.detectorList[4].pitchDeg=0.0

# Serial string associated with this specific detector
config.detectorList[4].serial='4'

# ID of detector slot
config.detectorList[4].id=4
# Name of this config
#This isn't strictly required for CameraMapper
#but I'm keeping it there as it seems like a good idea:
config.name='Goto'



