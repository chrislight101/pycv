import numpy as np
import cv2

#open feed and calculate center
cap0 = cv2.VideoCapture(0)
cap0.open(0)
ret ,frame = cap0.read()
cap1 = cv2.VideoCapture(1)
cap1.open(1)
ret ,frame = cap1.read()



while(True):
    ret0 ,frame0 = cap0.read()
    ret1 ,frame1 = cap1.read()
    img0 = cv2.cvtColor(frame0,cv2.COLOR_BGR2GRAY)  
    img1 = cv2.cvtColor(frame1,cv2.COLOR_BGR2GRAY)
    img0 = cv2.resize(img0, (0,0), fx=0.5, fy=0.5)
    img1 = cv2.resize(img1, (0,0), fx=0.5, fy=0.5)
    
    stereo = cv2.StereoSGBM(minDisparity=16,numDisparities=96,SADWindowSize=3)
    
    disparity = stereo.compute(img0, img1)
    
    #display and position window
    cv2.imshow('img',disparity)
    #cv2.moveWindow('img', 1200,240)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    
cap.release()
cv2.destroyAllWindows()
