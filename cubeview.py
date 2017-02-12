import numpy as np
import cv2

#open feed and calculate center
cap = cv2.VideoCapture(1)
cap.open(1)
ret ,frame = cap.read()
center_x, center_y = int(cap.get(3)/2),int(cap.get(4)/2)

#define regions of interest
topleft = frame[(center_y-150):(center_y-50),(center_x-150):(center_x-50)]
topcenter = frame[(center_y-150):(center_y-50),(center_x-50):(center_x+50)]
topright = frame[(center_y-150):(center_y-50),(center_x+50):(center_x+150)]
middleleft = frame[(center_y-50):(center_y+50),(center_x-150):(center_x-50)]
center = frame[(center_y-50):(center_y+50),(center_x-50):(center_x+50)]
middleright = frame[(center_y-50):(center_y+50),(center_x+50):(center_x+150)]
bottomleft = frame[(center_y+50):(center_y+150),(center_x-150):(center_x-50)]
bottomcenter = frame[(center_y+50):(center_y+150),(center_x-50):(center_x+50)]
bottomright = frame[(center_y+50):(center_y+150),(center_x+50):(center_x+150)]

while(True):
    #get frame and convert to HSV space
    ret ,frame = cap.read()
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
    
    #mask = mask_blue | mask_green | mask_white | mask_orange
    mask = mask_green
    res = cv2.bitwise_and(frame, frame, mask=mask)
    
    #res = frame
    #topleft = res[(center_y-150):(center_y-50),(center_x-150):(center_x-50)]



    mask = np.zeros(topleft.shape,np.uint8)
    #avgred = cv2.mean(topleft,mask = mask)
    
    color = "GREEN"
    #draw rectangles and text, show and reposition final image
    #cv2.imshow('img2',topright) #show ROI before the overlay
    cv2.rectangle(res, (center_x-150,center_y-150), (center_x+150,center_y+150), (0,255,255),1)
    cv2.rectangle(res, (center_x-150,center_y-150), (center_x-50,center_y-50), (0,255,255),1) #top left
    cv2.putText(res, color, ((center_x-125), (center_y-100)),cv2.FONT_HERSHEY_SIMPLEX,.5,(0,255,255),2)
    cv2.rectangle(res, (center_x-50,center_y-150), (center_x+50,center_y-50), (0,255,255),1) #top center
    cv2.putText(res, color, ((center_x-25), (center_y-100)),cv2.FONT_HERSHEY_SIMPLEX,.5,(0,255,255),2)
    cv2.rectangle(res, (center_x+50,center_y-150), (center_x+150,center_y-50), (0,255,255),1) #top right
    cv2.putText(res, color, ((center_x+75), (center_y-100)),cv2.FONT_HERSHEY_SIMPLEX,.5,(0,255,255),2)
    cv2.rectangle(res, (center_x-150,center_y-50), (center_x-50,center_y+50), (0,255,255),1) #middle left
    cv2.putText(res, color, ((center_x-125), (center_y)),cv2.FONT_HERSHEY_SIMPLEX,.5,(0,255,255),2)
    cv2.rectangle(res, (center_x-50,center_y-50), (center_x+50,center_y+50), (0,255,255),1) #center
    cv2.putText(res, color, ((center_x-25), (center_y)),cv2.FONT_HERSHEY_SIMPLEX,.5,(0,255,255),2)
    cv2.rectangle(res, (center_x+50,center_y-50), (center_x+150,center_y+50), (0,255,255),1) #middle right
    cv2.putText(res, color, ((center_x+75), (center_y)),cv2.FONT_HERSHEY_SIMPLEX,.5,(0,255,255),2)
    cv2.rectangle(res, (center_x-150,center_y+50), (center_x-50,center_y+150), (0,255,255),1) #bottom left
    cv2.putText(res, color, ((center_x-125), (center_y+100)),cv2.FONT_HERSHEY_SIMPLEX,.5,(0,255,255),2)
    cv2.rectangle(res, (center_x-50,center_y+50), (center_x+50,center_y+150), (0,255,255),1) #bottom center
    cv2.putText(res, color, ((center_x-25), (center_y+100)),cv2.FONT_HERSHEY_SIMPLEX,.5,(0,255,255),2)
    cv2.rectangle(res, (center_x+50,center_y+50), (center_x+150,center_y+150), (0,255,255),1) #bottom right
    cv2.putText(res, color, ((center_x+75), (center_y+100)),cv2.FONT_HERSHEY_SIMPLEX,.5,(0,255,255),2)

    #display and position window
    cv2.imshow('img',res)
    #cv2.imshow('img2',topleft) #show ROI after the overlay
    cv2.moveWindow('img', 1200,240)
    cv2.moveWindow('img2', 1200,240)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    
cap.release()
cv2.destroyAllWindows()
