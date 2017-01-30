import numpy as np
import cv2
import serial
import time

#open a serial port to talk to motor controller
#ser = serial.Serial('/dev/ttyACM0',96002,timeout=10)
time.sleep(1)

#open feed and calculate center
cap = cv2.VideoCapture(1)
cap.open(1)
ret ,frame = cap.read()
lb_green = np.array([45,75,75])
ub_green = np.array([70,255,255])

#setup trackbars for adjusting HSV values
def nothing(x):
    pass
cv2.namedWindow('img',0)
cv2.createTrackbar('HUE','img',0,255,nothing)
cv2.createTrackbar('SAT','img',0,255,nothing)
cv2.createTrackbar('VAL','img',0,255,nothing)
cv2.resizeWindow('img',640,480)

def contours(frame, img):
    #find the contours and moments of the threshdold image
    contours = cv2.findContours(img,1,2)
    area = cv2.contourArea(contours[0])
    print (str(area))
    M = cv2.moments(contours[0])
        
    #calculate center of mass of green blobs and draw target
    cx = int(M['m10']/M['m00'])
    cy = int(M['m01']/M['m00'])
    cv2.line(frame,(cx-20,cy),(cx+12,cy),(0,255,0,),5)
    cv2.line(frame,(cx,cy-20),(cx,cy+12),(0,255,0,),5)

while(True):
    #read frame from the webcam and convert image to HSV
    ret ,frame = cap.read()
    
    hsv = cv2.cvtColor(frame,cv2.COLOR_BGR2HSV) 
    
    #threshold to upper and lower green values 
    hue = cv2.getTrackbarPos('HUE','img')
    sat = cv2.getTrackbarPos('SAT','img') 
    val = cv2.getTrackbarPos('VAL','img') 
    
    lb_green = np.array([(hue-20),sat,val])
    ub_green = np.array([(hue+20),255,255]) 
    lb_green = np.array([45,75,75])
    ub_green = np.array([70,255,255])
    thresh = cv2.inRange(hsv, lb_green,ub_green)
    res = cv2.bitwise_and(frame, frame, mask=thresh)
    
    #find the contours and moments of the threshdold image
    contours = cv2.findContours(thresh,1,2)
    #area = cv2.contourArea(contours[0])
    print (str(contours[0]))
    M = cv2.moments(contours[0])
        
    #calculate center of mass of green blobs and draw target
    cx = int(M['m10']/M['m00'])
    cy = int(M['m01']/M['m00'])
    cv2.line(frame,(cx-20,cy),(cx+12,cy),(0,255,0,),5)
    cv2.line(frame,(cx,cy-20),(cx,cy+12),(0,255,0,),5)
    
    #display and position window in top-right
    
    cv2.imshow('img',frame)
    cv2.moveWindow('img', 0,0)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    
cap.release()
cv2.destroyAllWindows()
