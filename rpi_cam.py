import numpy as np
import cv2
import math

def rpiSetup():
	import RPi.GPIO as GPIO
	GPIO.setmode(GPIO.BCM)
	GPIO.setwarnings(False)
	GPIO.setup(11, GPIO.OUT) #in1
	GPIO.setup(12, GPIO.OUT) #in2
	GPIO.setup(13, GPIO.OUT) #in3
	GPIO.setup(15, GPIO.OUT) #in4

def captureSetup():
	cap = cv2.VideoCapture(1)
	ret ,img = cap.read()
	cv2.imshow('img',img)
	cv2.moveWindow('img', 0,0)
	return cap

def metrics(cap):
	h = cap.get(4)
	w = cap.get(3)
	cx, cy = int(w/2),int(h/2)
	return h, w, cx, cy

#left and right motor forward, back, and stop functions
def Lmtrfwd():
	GPIO.output(11, 1)
	GPIO.output(12, 0)
	
def Lmtrbk():
	GPIO.output(11, 0)
	GPIO.output(12, 1)

def Lmtrstp():
	GPIO.output(11, 0)
	GPIO.output(12, 0)
	
def Rmtrfwd():
	GPIO.output(13, 1)
	GPIO.output(15, 0)
	
def Rmtrbk():
	GPIO.output(13, 0)
	GPIO.output(15, 1)

def Rmtrstp():
	GPIO.output(13, 0)
	GPIO.output(15, 0)
	
def leftTurn():
    	textHUD('LEFT')
	#GPIO.output(18, 1)

def rightTurn():
    	textHUD('RIGHT')
	#GPIO.output(18, 0)

def textHUD(dirtext):
	font = cv2.FONT_HERSHEY_SIMPLEX
	cv2.putText(img, dirtext,(cx,cy),font,4,(0,255,255),2)

def process(frame):
	img = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
	img = cv2.GaussianBlur(img,(5,5),0)
	ret,img = cv2.threshold(img,127,255,cv2.THRESH_OTSU)
	l_img = img[0:h,0:cx]
	r_img = img[0:h,cx:w]
	is_left = np.average(l_img) > np.average(r_img)
	return img, is_left

#rpiSetup()
cap = captureSetup()
h, w, cx, cy = metrics(cap)
while(True):
    ret, frame = cap.read()
    img, left = process(frame)
    img = cv2.cvtColor(img,cv2.COLOR_GRAY2BGR)
    if left:
    	leftTurn()
    else:
    	rightTurn()
    cv2.imshow('img',img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
   
cap.release()
cv2.destroyAllWindows()
