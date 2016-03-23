import numpy as np
from matplotlib import pyplot as plt
import cv2

#open feed and calculate center
cap = cv2.VideoCapture(0)
cap.open(0)
ret ,frame = cap.read()
print(cap.isOpened())
#center_x, center_y = int(cap.get(3)/2),int(cap.get(4)/2)
fgbg = cv2.BackgroundSubtractorMOG2()

while(True):
    #get red frame
    ret ,frame = cap.read()
    img = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
    red = frame[:,:,2]

    #equalize histogram
    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8,8))
    #img = clahe.apply(img)
    #red = cv2.equalizeHist(red)

    #histograms
    #plt.hist(img,256, [0,256])
    #plt.show()
    
    
    #display and position window
    cv2.imshow('img',img)
    cv2.moveWindow('img', 1200,240)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    
cap.release()
cv2.destroyAllWindows()
