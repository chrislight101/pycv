import numpy as np
import cv2

#open feed and calculate center
cap = cv2.VideoCapture(0)
cap.open(0)
ret ,frame = cap.read()
print(cap.isOpened())
#center_x, center_y = int(cap.get(3)/2),int(cap.get(4)/2)


while(True):
    ret ,frame = cap.read()
    img = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)    
    
    #display and position window
    cv2.imshow('img',img)
    cv2.moveWindow('img', 1200,240)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    
cap.release()
cv2.destroyAllWindows()
