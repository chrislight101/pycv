import numpy as np
import cv2

###open feed and calculate center
cap = cv2.VideoCapture(0)
cap.open(0)
ret ,frame = cap.read()
center_x, center_y = int(cap.get(3)/2),int(cap.get(4)/2)

###UI trackbars for HSV threshold values
def nothing(x):
    pass
cv2.namedWindow('img',0)
cv2.createTrackbar('HUE','img',0,255,nothing)
cv2.createTrackbar('SAT','img',0,255,nothing)
cv2.createTrackbar('VAL','img',0,255,nothing)
cv2.resizeWindow('img',640,480)
lb = np.array([45,75,75])
ub = np.array([70,255,255])

def bounds():
    hue = cv2.getTrackbarPos('HUE','img')
    sat = cv2.getTrackbarPos('SAT','img') 
    val = cv2.getTrackbarPos('VAL','img') 
    
    lb = np.array([(hue-20),sat,val])
    ub = np.array([(hue+20),255,255])
    return lb, ub

###kernel for morphology
kernel = np.ones((3,3),np.uint8)

while(True):
    ###get frame and convert to HSV space
    ret ,frame = cap.read()
    hsv = cv2.cvtColor(frame,cv2.COLOR_BGR2HSV)
    
    lb,ub = bounds()
    green = cv2.inRange(hsv, lb,ub)
    blur = cv2.GaussianBlur(green,(5,5),0)    
    #res = cv2.bitwise_and(frame, frame, mask=thresh)
    #img = cv2.GaussianBlur(hsv,(5,5),0)
    #img = cv2.medianBlur(img,5)   
    #img = cv2.adaptiveThreshold(img,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,cv2.THRESH_BINARY,11,3.5)    
    #img = cv2.Canny(img,150,200)
    corners = cv2.cornerHarris(green,5,5,.1)    
    corners = cv2.goodFeaturesToTrack(corners,8,0.01,100)
    green = cv2.cvtColor(green,cv2.COLOR_GRAY2BGR)
    if corners is not None:
        corners = np.int0(corners)
        print corners.ndim
        print "\n"
        for i in corners:
            x,y = i.ravel()
            cv2.circle(frame,(x,y),5,(255,0,255),-1)
    
    #open = cv2.morphologyEx(corners, cv2.MORPH_OPEN, kernel)
    cv2.circle(frame,(200,100),10,(255,0,255),-1)
    blur = cv2.cvtColor(blur,cv2.COLOR_GRAY2BGR)
    final = np.concatenate((frame, hsv, blur),axis=1)
    
    ###display and position window
    cv2.imshow('img',final)
    cv2.moveWindow('img', 0,0)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    
cap.release()
cv2.destroyAllWindows()