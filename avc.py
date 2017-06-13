import numpy as np
import cv2

#open feed and calculate center
cap = cv2.VideoCapture(0)
cap.open(0)
ret ,frame = cap.read()
print(cap.isOpened())
#center_x, center_y = int(cap.get(3)/2),int(cap.get(4)/2)


while(True):
    #get frame and convert to HSV space
    ret ,frame = cap.read()
    frame = cv2.resize(frame,(0,0), fx=.5, fy=.5)
    img = cv2.cvtColor(frame,cv2.COLOR_BGR2HSV)

    #define color masks and bitwise AND operation
    lb_blue = np.array([110,50,50])
    ub_blue = np.array([130,255,255])
    mask_blue = cv2.inRange(img, lb_blue, ub_blue)
    lb_green = np.array([45,50,50])
    ub_green = np.array([70,255,255])
    mask_green = cv2.inRange(img, lb_green, ub_green)
    lb_white = np.array([0,0,200])
    ub_white = np.array([179,25,255])
    mask_white = cv2.inRange(img, lb_white, ub_white)
    lb_orange = np.array([10,50,50])
    ub_orange = np.array([18,255,255])
    mask_orange = cv2.inRange(img, lb_orange, ub_orange)  
    
    mask = mask_blue
    res = cv2.bitwise_and(frame, frame, mask=mask)
    
    #display and position window
    cv2.imshow('img',res)
    #cv2.moveWindow('img', 1200,240)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    
cap.release()
cv2.destroyAllWindows()
