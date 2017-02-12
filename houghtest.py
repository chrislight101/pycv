import numpy as np
import cv2

#open feed and calculate center
cap = cv2.VideoCapture(0)
cap.open(0)
ret ,frame = cap.read()
center_x, center_y = int(cap.get(3)/2),int(cap.get(4)/2)
print(cap.isOpened())
while(True):
    ret ,frame = cap.read()
    img = frame
    gray = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
    edges = cv2.Canny(gray,50,150,apertureSize = 3)
    circles = cv2.HoughCircles(edges,cv2.HOUGH_GRADIENT,1,20,param1=50,param2=30,minRadius=0,maxRadius=0)
    circles = np.uint16(np.around(circles))
    for i in circles[0,:]:
        cv2.circle(img,(i[0],i[1]),i[2],(0,255,0),2)
        cv2.circle(img,(i[0],i[1]),2,(0,0,255),3)
		

    #display and position window
    cv2.imshow('img',img)
    cv2.moveWindow('img', 1200,240)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    
cap.release()
cv2.destroyAllWindows()
