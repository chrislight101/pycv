import numpy as np
import cv2
import math as m
import time

pts1 = np.float32([[10,10],[10,50],[50,10],[50,50]])
pts2 = np.float32([[210,210],[210,250],[250,220],[240,240]])
pts2 = np.float32([[10,10],[10,50],[50,10],[50,50]])

#create image
img = np.zeros((480,640),dtype=np.float32)
img = cv2.cvtColor(img,cv2.COLOR_GRAY2BGR)

#starting points
p = np.array([[10,10,1],
              [10,50,1],
              [50,10,1],
              [50,50,1]],dtype=np.uint8)
          
#observed points    
c = np.array([[210,210,1],
              [210,250,1],
              [250,220,1],
              [250,240,1]],dtype=np.uint8)


#rotation angle in radians
t = m.pi / 4
#rotation translation matrix
R = np.array([[m.cos(t),-1*m.sin(t),100],
                [m.sin(t),m.cos(t),100]])
#affine matrix               
A = np.array([[1.266,0.6,100],
                [-0.333,1,100]])


def drawpoints():
    #draw start and end points
    for row in pts1:
        #d = np.int0(np.dot(A,row))
        cv2.circle(img,(row[0],row[1]),5,(0,255,0),-1) #model points
        #cv2.circle(img,(d[0],d[1]),5,(0,0,255),-1) #transformed points
        
    for row in pts2:    
        cv2.circle(img,(row[0],row[1]),5,(255,0,255),-1) #observed points

for i in range(1,20):   
    pts2 = pts2 + i
    M = cv2.getPerspectiveTransform(pts1,pts2)
    print M
    
    drawpoints()
    cv2.imshow('img',img)
    cv2.waitKey(1)
    time.sleep(1)
    img[:] = (0, 0, 0)


#display image
cv2.imshow('img',img)
cv2.waitKey(1)
cv2.destroyAllWindows()
