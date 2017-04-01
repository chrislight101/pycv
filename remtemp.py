import numpy as np
import cv2
import time
import timeit

#open feed and calculate center
cap = cv2.VideoCapture(1)
cap.open(1)
ret ,frame = cap.read()
ret ,frame = cap.read()
ret ,frame = cap.read()
print(cap.isOpened())
h = int(cap.get(4))
w = int(cap.get(3))
cx,cy = int(cap.get(3)/2),int(cap.get(4)/2)
timeconst = 1491000000
timestart = time.time()
f = open('data.csv','w')

while(True):
    ret ,frame = cap.read()
    frame = cv2.resize(frame,(0,0), fx=.5, fy=.5)
   
   
   
    
    
    img = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
    ret,img = cv2.threshold(img,50,255,cv2.THRESH_BINARY)
    l_avg, r_avg = np.average(img[0:h,0:cx]), np.average(img[0:h,cx:w])
    avg = np.average(img)
 
 
 
 
 
 
    
    img = cv2.cvtColor(img,cv2.COLOR_GRAY2BGR)
    font = cv2.FONT_HERSHEY_SIMPLEX
    txt = str(timeit.timeit())
    f.write(str(time.time()-timestart) + ',' + str(avg) + '\r\n')
    cv2.putText(img, txt,(30,30),font,0.9,(0,0,255),2)    
    #display and position window
    cv2.imshow('img',img)
    #cv2.moveWindow('img', 1200,240)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

f.close()    
cap.release()
cv2.destroyAllWindows()
