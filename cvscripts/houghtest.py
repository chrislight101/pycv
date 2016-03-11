import numpy as np
import cv2

#open feed and calculate center
cap = cv2.VideoCapture(1)
cap.open(1)
ret ,frame = cap.read()
center_x, center_y = int(cap.get(3)/2),int(cap.get(4)/2)
print(cap.isOpened())
while(True):
    ret ,frame = cap.read()
    img = frame
    gray = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
    edges = cv2.Canny(gray,50,150,apertureSize = 3)
    minLineLength = 100
    maxLineGap = 1
    lines = cv2.HoughLinesP(edges,1,np.pi/180,100,minLineLength,maxLineGap)
    for x1,y1,x2,y2 in lines[0]:
        cv2.line(img,(x1,y1),(x2,y2),(0,255,0),2)

    #display and position window
    cv2.imshow('img',img)
    cv2.moveWindow('img', 1200,240)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    
cap.release()
cv2.destroyAllWindows()
