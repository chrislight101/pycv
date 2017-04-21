import cv2
import numpy as np
import time
from collections import deque
import picamera
from picamera import PiCamera
from picamera.array import PiRGBArray

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
timeout = 100
avgcenter = 160
timestart = time.time()
samples = deque(np.zeros(100))

#GPIO PWM setup
import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)
GPIO.setup(11,GPIO.OUT)
p = GPIO.PWM(11,50)
p.start(50)

#video writing
out = cv2.VideoWriter('output.avi',-1,20.0,(320,240))
f = open('data.csv','w')

#LED pulse function        
def led(pwm,pulsems,duration):
    ledstart = time.time()
    pulsems = float(pulsems / 1000.)
    while(time.time() - ledstart < duration):
        p.ChangeDutyCycle(pwm)
        time.sleep(pulsems)
        p.ChangeDutyCycle(0)
        time.sleep(pulsems)
    
    p.ChangeDutyCycle(0)

###MAINLOOP###    
for frame in camera.capture_continuous(rawCapture, format='bgr',use_video_port=True):
    frame = frame.array
    #resize frame
    frame = cv2.resize(frame,(0,0), fx=0.25, fy=0.25)
   
    #convert to grayscale, threshold, averaging
    img = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
    ret,img = cv2.threshold(img,thresh,255,cv2.THRESH_BINARY)
    avg = np.average(img)
    samples.append(avg)
    samples.popleft()
    ma = np.average(samples)

    #LED pulse triggering
    if (ma>200 and LEDon and timeout > 100):
        triggered = True
        led(50,500,5) # 500ms pulses at 50% for 2 seconds
        timeout = 0
    timeout = timeout + 1
  
    #convert back to BGR for color text display
    img = cv2.cvtColor(img,cv2.COLOR_GRAY2BGR)
    font = cv2.FONT_HERSHEY_SIMPLEX
    f.write(str(time.time()-timestart) + ',' + str(avg) + '\r\n')
    txt = str(avg)
    cv2.putText(img, txt,(30,30),font,0.7,(0,0,255),2)    

    #keyboard commands for frame capture and manual thresholding
    key = cv2.waitKey(1) & 0xFF
    if key == ord('x'):
        cv2.imwrite('../frame' + str(imwritecounter) + '.png',img)
        imwritecounter = imwritecounter + 1
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
        triggered = True
        if avg < avgcenter:
            thresh = thresh - 2
        if avg > avgcenter:
            thresh = thresh + 2
    
    #autothreshold    
    if autothreshold:
        if avg < avgcenter:
            thresh = thresh - 2
        if avg > avgcenter:
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
