import numpy as np
import cv2
import math
import RPi.GPIO as GPIO

def thresh(image):
	img = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
	img = cv2.GaussianBlur(img,(5,5),0)
	ret2,img = cv2.threshold(img,127,255,cv2.THRESH_OTSU)
	return img

#open feed and calculate center
cap = cv2.VideoCapture(0)
cap.open(0)
ret ,frame = cap.read()
height = cap.get(4)
width = cap.get(3)
center_x, center_y = int(width/2),int(height/2)
img = frame
cv2.imshow('img',img)
cv2.moveWindow('img', 0,0)

#GPIO setup
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(18, GPIO.OUT)

while(True):
    #get frame and convert to HSV space
    ret ,frame = cap.read()
    img = thresh(frame)
    leftimg = img[0:height,0:center_x]
    rightimg = img[0:height,center_x:width]
    if np.average(leftimg) > np.average(rightimg):
    	dirtext = 'LEFT'
	GPIO.output(18, 1)
    else:
    	dirtext = 'RIGHT'
	GPIO.output(18, 0)
    
    img = cv2.cvtColor(img,cv2.COLOR_GRAY2BGR)
    font = cv2.FONT_HERSHEY_SIMPLEX
    cv2.putText(img, dirtext,(center_x,center_y),font,4,(0,255,255),2)
    #display and position window
    cv2.imshow('img',img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
   
cap.release()
cv2.destroyAllWindows()
