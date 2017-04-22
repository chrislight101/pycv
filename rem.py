import cv2
import numpy as np
import time
from collections import deque
import picamera
from picamera import PiCamera
from picamera.array import PiRGBArray
import pygame

#camera module setup
h = 640
w = 480
camera = PiCamera()
camera.resolution = (h,w)
camera.framerate = 30
rawCapture = PiRGBArray(camera,size=(h,w))

#main variables
imwritecounter = 1
thresh = 160
autothreshold = True
LEDon = False
filewrite = False
timeout = 100
avgcenter = 160
timestart = time.time()
samples = deque(np.zeros(50))

#GPIO PWM setup
import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)
GPIO.setup(11,GPIO.OUT)
p = GPIO.PWM(11,10)
p.start(0)

#video writing
out = cv2.VideoWriter('output.avi',-1,20.0,(320,240))
f = open('data.csv','w')
f.write('Time,Average,MvgAvg,Sum,Stddev\r\n')

###MAINLOOP###    
for frame in camera.capture_continuous(rawCapture, format='bgr',use_video_port=True):
    frame = frame.array
    #resize frame
    frame = cv2.resize(frame,(0,0), fx=0.25, fy=0.25)
   
    #convert to grayscale, threshold, averaging
    img = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
    ret,img = cv2.threshold(img,25,255,cv2.THRESH_BINARY)

    avg = np.mean(img)
    imsum = np.sum(img)
    std = np.std(img)

    samples.append(imsum)
    samples.popleft()
    ma = np.average(samples)

    print(str(np.std(samples) / 1000))

    #LED pulse triggering
    if (ma>200 and LEDon and timeout > 100):
        p.ChangeDutyCycle(50)
        time.sleep(5)
        p.ChangeDutyCycle(0)
        timeout = 0
    timeout = timeout + 1
  
    #convert back to BGR for color text display
    img = cv2.cvtColor(img,cv2.COLOR_GRAY2BGR)
    font = cv2.FONT_HERSHEY_SIMPLEX

    timestr =  str(time.time()-timestart)
    if filewrite:
        f.write(timestr + ',' + str(avg) + ',' + str(ma) +  ',' + str(imsum) + ',' + str(std) + '\r\n')

    cv2.putText(img, str(avg),(30,30),font,0.7,(0,0,255),2)    

    #keyboard commands for frame capture and manual thresholding
    key = cv2.waitKey(1) & 0xFF
    if key == ord('x'):
        cv2.imwrite('../frame' + str(imwritecounter) + '.png',img)
        imwritecounter = imwritecounter + 1
    if key == ord('w'):
        filewrite = True
    if not autothreshold:
        if key == ord('i'):
            thresh = thresh + 5
        if key == ord('k'):
            thresh = thresh - 5
    else:
        if key == ord('i'):
            avgcenter = avgcenter + 5
        if key == ord('k'):
            avgcenter = avgcenter - 5
        if avg < avgcenter:
            thresh = thresh - 2
        if avg > avgcenter + 1:
            thresh = thresh + 2
    
    

    #display and position window
    cv2.imshow('img',img)
    cv2.moveWindow('img',0,0)
    rawCapture.truncate(0)
    if key == ord('q'):
        break

p.stop
GPIO.cleanup()
f.close()        
out.release()
cv2.destroyAllWindows()
