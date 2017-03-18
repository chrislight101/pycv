import numpy as np
import cv2
import serial
import math
import time

def captureSetup(cap_in):
    cap = cv2.VideoCapture(cap_in)
    ret ,img = cap.read()
    h = int(cap.get(4))
    w = int(cap.get(3))
    cx, cy = int(w/2),int(h/2)
    return cap, h, w, cx, cy

###UI trackbars for HSV threshold values
def nothing(x):
    pass

def createtrackbars():
    cv2.namedWindow('img',0)
    cv2.createTrackbar('HUE','img',0,255,nothing)
    cv2.createTrackbar('SAT','img',0,255,nothing)
    cv2.createTrackbar('VAL','img',0,255,nothing)

def bounds2():
    lb = np.array([45,75,75])
    ub = np.array([70,255,255])
    return lb, ub

def bounds():
    hue = cv2.getTrackbarPos('HUE','img')
    sat = cv2.getTrackbarPos('SAT','img') 
    val = cv2.getTrackbarPos('VAL','img') 
    lb = np.array([(hue-20),sat,val])
    ub = np.array([(hue+20),255,255])
    return lb, ub

def textHUD(txt, y):
    font = cv2.FONT_HERSHEY_SIMPLEX
    cv2.putText(img, txt,(10,y),font,0.5,(0,255,255),1)

def process(frame):
    hsv = cv2.cvtColor(frame,cv2.COLOR_BGR2HSV)
    lb,ub = bounds2()
    img = cv2.inRange(hsv, lb,ub)
    kernel = np.ones((3,3),np.uint8)
    img = cv2.morphologyEx(img, cv2.MORPH_OPEN, kernel)
    img = cv2.GaussianBlur(img,(5,5),0)
    x = img

    l_avg, r_avg = np.average(img[0:h,0:cx]), np.average(img[0:h,cx:w])
    img = cv2.cvtColor(img,cv2.COLOR_GRAY2BGR)
    return img, l_avg, r_avg

def motorsetup():
    global p, q
    import RPi.GPIO as GPIO
    GPIO.setmode(GPIO.BOARD)
    GPIO.setwarnings(False)
    #motor 1 pins
    GPIO.setup(11,GPIO.OUT) # A PWM
    GPIO.setup(13,GPIO.OUT) 
    GPIO.setup(15,GPIO.OUT)
    p = GPIO.PWM(11,50)
    #motor 2 pins
    GPIO.setup(12,GPIO.OUT) # B PWM
    GPIO.setup(16,GPIO.OUT)
    GPIO.setup(18,GPIO.OUT)
    q = GPIO.PWM(18,50)

    p.start(0)
    q.start(0)
    GPIO.output(13,0)
    GPIO.output(15,1)
    GPIO.output(12,1)
    GPIO.output(16,0)
    
def motorcontrol(l_avg,r_avg):
    l_pwm = int(100*(math.fabs(l_avg - 15)/(30)))
    r_pwm = int(100*(math.fabs(r_avg - 15)/(30)))

    # restrict PWM to between 0 and 100 duty cycle
    if (l_pwm < 0):
        l_pwm = 0
    if (l_pwm > 100):
        l_pwm = 100

    if (r_pwm < 0):
        r_pwm = 0
    if (r_pwm > 100):
        r_pwm = 100

    # add deadband for centered targets
    if (l_avg < 15 and l_avg > 11):
        l_pwm = 0

    if (r_avg < 15 and r_avg > 11):
        r_pwm = 0

    p.ChangeDutyCycle(l_pwm)
    q.ChangeDutyCycle(r_pwm)
    return l_pwm, r_pwm

###### MAIN LOOP ######
#createtrackbars()
motorsetup()
cap, h, w, cx, cy = captureSetup(0)
while(True):
    ret, frame = cap.read()
    img, l_avg, r_avg = process(frame)
    
    l_pwm, r_pwm = motorcontrol(l_avg,r_avg)


    textHUD('LAVG: '+str(l_avg),20)
    textHUD('RAVG: '+str(r_avg),40)
    textHUD('LPWM: '+str(l_pwm),60)
    textHUD('RPWM: '+str(r_pwm),80)

    cv2.imshow('img',img)
    cv2.waitKey(1)

cap.release()
cv2.destroyAllWindows()
