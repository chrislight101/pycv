import cv2
import numpy as np
from picamera import PiCamera
from picamera.array import PiRGBArray

h = 320
w = 240
camera = PiCamera()
camera.resolution = (h,w)
camera.framerate = 30
rawCapture = PiRGBArray(camera,size=(h,w))


for frame in camera.capture_continuous(rawCapture, format='bgr',use_video_port=True):
	frame = frame.array

	###get frame and convert
	frame = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)

	cv2.imshow('img',frame)
	#cv2.moveWindow('img',0,0)
	key = cv2.waitKey(1) & 0xFF
	rawCapture.truncate(0)
	if key == ord('q'):
		break


