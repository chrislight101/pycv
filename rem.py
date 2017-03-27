import cv2
import numpy as np
import picamera
from picamera import PiCamera
from picamera.array import PiRGBArray

h = 160
w = 120
camera = PiCamera()
camera.resolution = (h,w)
camera.framerate = 30
rawCapture = PiRGBArray(camera,size=(h,w))

for frame in camera.capture_continuous(rawCapture, format='bgr',use_video_port=True):
    frame = frame.array
    
    img = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
    ret,img = cv2.threshold(img,50,255,cv2.THRESH_BINARY)
    #kernel = np.ones((3,3,np.uint8)
    #img = cv2.morphologyEx(img, cv2.MORPH_OPEN, kernel)

    cv2.imshow('img',img)
    #cv2.moveWindow('img',0,0)
    key = cv2.waitKey(1) & 0xFF
    rawCapture.truncate(0)
    if key == ord('q'):
        break
