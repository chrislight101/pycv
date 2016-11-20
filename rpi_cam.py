import numpy as np
import cv2
import math
#import RPi.GPIO as GPIO

def process(image):
	img = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
	img = cv2.GaussianBlur(img,(5,5),0)
	ret2,img = cv2.threshold(img,127,255,cv2.THRESH_OTSU)
	leftimg = img[0:height,0:center_x]
	rightimg = img[0:height,center_x:width]
	is_left = np.average(leftimg) > np.average(rightimg)
	return img, is_left

def rpiSetup():
	import RPi.GPIO as GPIO
	GPIO.setmode(GPIO.BCM)
	GPIO.setwarnings(False)
	GPIO.setup(18, GPIO.OUT)

def captureSetup():
	cap = cv2.VideoCapture(1)
	cap.open(1)
	ret ,img = cap.read()
	cv2.imshow('img',img)
	cv2.moveWindow('img', 0,0)
	return cap

def leftTurn():
    	textHUD('LEFT')
	#GPIO.output(18, 1)

def rightTurn():
    	textHUD('RIGHT')
	#GPIO.output(18, 0)

def textHUD(dirtext):
	font = cv2.FONT_HERSHEY_SIMPLEX
	cv2.putText(img, dirtext,(center_x,center_y),font,4,(0,255,255),2)

#rpiSetup()
cap = captureSetup()
height = cap.get(4)
width = cap.get(3)
center_x, center_y = int(width/2),int(height/2)

while(True):
    #get frame and convert to HSV space
    ret ,frame = cap.read()
    img, left = process(frame)
    img = cv2.cvtColor(img,cv2.COLOR_GRAY2BGR)
    if left:
    	leftTurn()
    else:
    	rightTurn()

    #display and position window
    cv2.imshow('img',img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
   
cap.release()
cv2.destroyAllWindows()
