import cv2
import numpy as np
import time
import picamera
from picamera import PiCamera
from picamera.array import PiRGBArray

h = 160
w = 120
camera = PiCamera()
camera.resolution = (h,w)
camera.framerate = 30
rawCapture = PiRGBArray(camera,size=(h,w))

out = cv2.VideoWriter('output.avi',-1,20.0,(320,240))
timestart = time.time()
f = open('data.csv','w')

for frame in camera.capture_continuous(rawCapture, format='bgr',use_video_port=True):
    frame = frame.array
    #resize function if needed
    frame = cv2.resize(frame,(0,0), fx=0.5, fy=0.5)
    
    
    
    img = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
    ret,img = cv2.threshold(img,50,255,cv2.THRESH_BINARY)
    avg = np.average(img)





    img = cv2.cvtColor(img,cv2.COLOR_GRAY2BGR)
    font = cv2.FONT_HERSHEY_SIMPLEX
    f.write(str(time.time()-timestart) + ',' + str(avg) + '\r\n')
    txt = str(avg)
    cv2.putText(img, txt,(30,30),font,0.9,(0,0,255),2)    
    cv2.imshow('img',img)
    #cv2.moveWindow('img',0,0)
    key = cv2.waitKey(1) & 0xFF
    rawCapture.truncate(0)
    if key == ord('q'):
        break

f.close()        
out.release()
cv2.destroyAllWindows()
