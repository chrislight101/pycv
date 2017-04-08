import cv2
import numpy as np
import picamera
from picamera import PiCamera
from picamera.array import PiRGBArray

h = 320
w = 240
points = []
kernel = np.ones((3,3),np.uint8)
model = np.zeros((100,100))
model[48:52,48:52] = 1
camera = PiCamera()
camera.resolution = (h,w)
camera.framerate = 30
rawCapture = PiRGBArray(camera,size=(h,w))


for frame in camera.capture_continuous(rawCapture, format='bgr',use_video_port=True):
	frame = frame.array

	###get frame and convert to HSV space
	frame = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)




	cv2.imshow('img',frame)
	#cv2.moveWindow('img',0,0)
	key = cv2.waitKey(1) & 0xFF
	rawCapture.truncate(0)
	if key == ord('q'):
		break


