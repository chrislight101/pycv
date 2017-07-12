import numpy as np
import cv2

###open feed and calculate center
cap = cv2.VideoCapture(0)
cap.open(0)
ret ,frame = cap.read()
#center_x, center_y = int(cap.get(3)/2),int(cap.get(4)/2)

###define color mask bounds in HSV space (0-179,0-255,0-255)
lb_blue = np.array([60,0,0])
ub_blue = np.array([130,255,255])
lb_green = np.array([40,0,0])
ub_green = np.array([70,255,255])
lb_red = np.array([0,0,0])
ub_red = np.array([15,255,255])

###morphological kernel
kernel = np.ones((3,3),np.uint8)

###UI trackbars for HSV threshold values
def nothing(x):
	pass
cv2.namedWindow('img',0)
cv2.createTrackbar('HUE','img',0,179,nothing)
#cv2.createTrackbar('SAT','img',0,255,nothing)
#cv2.createTrackbar('VAL','img',0,255,nothing)

def bounds():
    hue = cv2.getTrackbarPos('HUE','img')
    #sat = cv2.getTrackbarPos('SAT','img') 
    #val = cv2.getTrackbarPos('VAL','img') 
    lb = np.array([(hue-20),0,0])
    ub = np.array([(hue+20),255,255])
    return lb, ub

while(True):
    ###get frame and convert to HSV space
    ret ,frame = cap.read()
    frame = cv2.resize(frame,(0,0), fx=.5, fy=.5)
    img = cv2.cvtColor(frame,cv2.COLOR_BGR2HSV)

    lb,ub = bounds()
    mask = cv2.inRange(img, lb,ub)
    #mask_blue = cv2.inRange(img, lb_blue, ub_blue)
    #mask_green = cv2.inRange(img, lb_green, ub_green)
    #mask_red = cv2.inRange(img, lb_red, ub_red)
    res = cv2.bitwise_and(frame, frame, mask=mask)   
    #res = cv2.morphologyEx(res, cv2.MORPH_OPEN, kernel)
    res = cv2.GaussianBlur(res,(5,5),0)
    #res = cv2.Canny(res,175,200)
    
    ###contours, moments, centroid
    #contours = cv2.findContours(mask,1,2)
    #print(contours)
    #cnt = contours[0]
    #M = cv2.moments(cnt)
    #cx = int(M['m10']/M['m00'])
    #cy = int(M['m01']/M['m00'])
    #mask = cv2.cvtColor(mask,cv2.COLOR_GRAY2BGR)
    #cv2.line(img,(cx-20,cy),(cx+20,cy),50)
    #cv2.line(img,(cx,cy-20),(cx,cy+20),50)
    
    
    ###display and position window
    #cv2.resizeWindow('img',320,240)
    
    final = np.concatenate((frame, mask),axis=1)   
    cv2.imshow('img',final)
    #cv2.moveWindow('img', 1200,240)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    
cap.release()
cv2.destroyAllWindows()
