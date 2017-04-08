import cv2
import numpy as np
import time
from collections import deque
import picamera
from picamera import PiCamera
from picamera.array import PiRGBArray

h = 640
w = 480
camera = PiCamera()
camera.resolution = (h,w)
camera.framerate = 30
rawCapture = PiRGBArray(camera,size=(h,w))
counter = 1
thresh = 50


import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)
GPIO.setup(11,GPIO.OUT)
p = GPIO.PWM(11,50)
p.start(0)


out = cv2.VideoWriter('output.avi',-1,20.0,(320,240))
timestart = time.time()
f = open('data.csv','w')
samples = deque(np.zeros(100))

def autothresh(frame):
    global thresh
    ret,img = cv2.threshold(frame,thresh,255,cv2.THRESH_BINARY)
    avg = np.average(img)
    while (avg < 200 and avg > 125):
        cv2.imshow('img',img)
        avg = np.average(img)
        if (avg < 125):
            thresh = thresh + 1
        

def led(pwm,pulsems,duration):
    ledstart = time.time()
    pulsems = float(pulsems / 1000.)
    while(time.time() - ledstart < duration):
        p.ChangeDutyCycle(pwm)
        time.sleep(pulsems)
        p.ChangeDutyCycle(0)
        time.sleep(pulsems)
    
    p.ChangeDutyCycle(0)
    

for frame in camera.capture_continuous(rawCapture, format='bgr',use_video_port=True):
    frame = frame.array
    #resize function if needed
    frame = cv2.resize(frame,(0,0), fx=0.25, fy=0.25)
   
    
    img = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
    ret,img = cv2.threshold(img,thresh,255,cv2.THRESH_BINARY)
    avg = np.average(img)
    samples.append(avg)
    samples.popleft()
    ma = np.average(samples)

    #if (ma>200):
        #led(50,500,10) # 100ms pulses at 50% for 2 seconds
    
  
    
    img = cv2.cvtColor(img,cv2.COLOR_GRAY2BGR)
    font = cv2.FONT_HERSHEY_SIMPLEX
    f.write(str(time.time()-timestart) + ',' + str(avg) + '\r\n')


    txt = str(avg)
    cv2.putText(img, txt,(30,30),font,0.7,(0,0,255),2)    


    cv2.imshow('img',img)
    cv2.moveWindow('img',0,0)
    key = cv2.waitKey(1) & 0xFF
    rawCapture.truncate(0)
    if key == ord('x'):
        cv2.imwrite('../frame' + str(counter) + '.png',img)
        counter = counter + 1
    if key == ord('i'):
        thresh = thresh + 5
    if key == ord('k'):
        thresh = thresh - 5
    if avg < 127:
        thresh = thresh - 2
    if avg > 128:
        thresh = thresh + 2
    if key == ord('q'):
        break

p.stop
GPIO.cleanup()
f.close()        
out.release()
cv2.destroyAllWindows()
