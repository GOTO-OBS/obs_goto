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
config.detectorList[0].name='g7_goto'

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
config.detectorList[0].serial='7'

# ID of detector slot
config.detectorList[0].id=7


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
config.detectorList[1].name='g6_goto'

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
config.detectorList[1].serial='6'

# ID of detector slot
config.detectorList[1].id=6


config.detectorList[2]=lsst.afw.cameraGeom.cameraConfig.DetectorConfig()

#All non-commented lines ARE REQUIRED for CameraMapper:
# y0 of pixel bounding box
config.detectorList[2].bbox_y0=0

# y1 of pixel bounding box
config.detectorList[2].bbox_y1=6131

# x1 of pixel bounding box
config.detectorList[2].bbox_x1=8175

# x0 of pixel bounding box
config.detectorList[2].bbox_x0=0

# Name of detector slot
config.detectorList[2].name='g3_goto'

# Pixel size in mm
config.detectorList[2].pixelSize_x=0.006
config.detectorList[2].pixelSize_y=0.006

# Name of native coordinate system
config.detectorList[2].transformDict.nativeSys='Pixels'

# x position of the reference point in the detector in pixels in transposed coordinates.
config.detectorList[2].refpos_x=4087.5

# y position of the reference point in the detector in pixels in transposed coordinates.
config.detectorList[2].refpos_y=3065.5

# Detector type: SCIENCE=0, FOCUS=1, GUIDER=2, WAVEFRONT=3
config.detectorList[2].detectorType=0

# x offset from the origin of the camera in mm in the transposed system.
config.detectorList[2].offset_x=0.

# y offset from the origin of the camera in mm in the transposed system.
config.detectorList[2].offset_y=0.

config.detectorList[2].yawDeg=0.0
config.detectorList[2].rollDeg=0.0
config.detectorList[2].pitchDeg=0.0

# Serial string associated with this specific detector
config.detectorList[2].serial='3'

# ID of detector slot
config.detectorList[2].id=3

config.detectorList[3]=lsst.afw.cameraGeom.cameraConfig.DetectorConfig()

#All non-commented lines ARE REQUIRED for CameraMapper:
# y0 of pixel bounding box
config.detectorList[3].bbox_y0=0

# y1 of pixel bounding box
config.detectorList[3].bbox_y1=6131

# x1 of pixel bounding box
config.detectorList[3].bbox_x1=8175

# x0 of pixel bounding box
config.detectorList[3].bbox_x0=0

# Name of detector slot
config.detectorList[3].name='g2_goto'

# Pixel size in mm
config.detectorList[3].pixelSize_x=0.006
config.detectorList[3].pixelSize_y=0.006

# Name of native coordinate system
config.detectorList[3].transformDict.nativeSys='Pixels'

# x position of the reference point in the detector in pixels in transposed coordinates.
config.detectorList[3].refpos_x=4087.5

# y position of the reference point in the detector in pixels in transposed coordinates.
config.detectorList[3].refpos_y=3065.5

# Detector type: SCIENCE=0, FOCUS=1, GUIDER=2, WAVEFRONT=3
config.detectorList[3].detectorType=0

# x offset from the origin of the camera in mm in the transposed system.
config.detectorList[3].offset_x=0.

# y offset from the origin of the camera in mm in the transposed system.
config.detectorList[3].offset_y=0.

config.detectorList[3].yawDeg=0.0
config.detectorList[3].rollDeg=0.0
config.detectorList[3].pitchDeg=0.0

# Serial string associated with this specific detector
config.detectorList[3].serial='2'

# ID of detector slot
config.detectorList[3].id=2
# Name of this config
#This isn't strictly required for CameraMapper
#but I'm keeping it there as it seems like a good idea:
config.name='Goto'



