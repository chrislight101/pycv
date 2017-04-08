import numpy as np
import cv2
import time
import timeit
from collections import deque

#open feed and calculate center
cap = cv2.VideoCapture(1)
cap.open(1)
ret ,frame = cap.read()
ret ,frame = cap.read()
ret ,frame = cap.read()
frame = cv2.resize(frame,(0,0), fx=.5, fy=.5)
print(cap.isOpened())
h = int(cap.get(4))
w = int(cap.get(3))
cx,cy = int(cap.get(3)/2),int(cap.get(4)/2)
height, width, layers = frame.shape
timeconst = 1491000000
timestart = time.time()
f = open('data.csv','w')
font = cv2.FONT_HERSHEY_SIMPLEX
samples = deque(np.zeros(100))
thresh = 50
autothreshold = True
imwritecounter = 0


fourcc = cv2.VideoWriter_fourcc(*'WMV1')
out = cv2.VideoWriter('vid.avi',fourcc,20.0,(width,height))

while(True):
    ret ,frame = cap.read()
    frame = cv2.resize(frame,(0,0), fx=.5, fy=.5)
    background = cv2.imread('../frame0.png')
    background = cv2.cvtColor(background,cv2.COLOR_BGR2GRAY)
    
    
    img = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
    img = abs(img-background)
    #img = cv2.GaussianBlur(img,(5,5),0)
    ret,img = cv2.threshold(img,thresh,255,cv2.THRESH_BINARY)
    #l_avg, r_avg = np.average(img[0:h,0:cx]), np.average(img[0:h,cx:w])
    avg = np.average(img)
    samples.append(avg)
    samples.popleft()
    ma = np.average(samples)
 
    out.write(img)
 
     #autothreshold    
    if autothreshold:
        if avg < 127:
            thresh = thresh - 2
        if avg > 127:
            thresh = thresh + 2

    key = cv2.waitKey(1) & 0xFF
    if key == ord('x'):
        cv2.imwrite('../frame' + str(imwritecounter) + '.png',frame)
        imwritecounter = imwritecounter
    
    img = cv2.cvtColor(img,cv2.COLOR_GRAY2BGR)  
    txt = str(ma)
    #txt = str(timeit.timeit())
    f.write(str(time.time()-timestart) + ',' + str(avg) + '\r\n')
    cv2.putText(img, txt,(30,30),font,0.9,(0,0,255),2)    
    #display and position window
    cv2.imshow('img',img)
    #cv2.moveWindow('img', 1200,240)
    if key == ord('q'):
        break

f.close()  
out.release()  
cap.release()
cv2.destroyAllWindows()
