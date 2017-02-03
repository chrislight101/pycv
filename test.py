import numpy as np
import cv2

a = np.array([[1,1,1],[1,0.5,1],[1,1,1]],dtype=np.float32)
print a.dtype
#a = np.ones((100,100))
#a[0:50,0:100] = 0
cv2.imshow('img',a)
cv2.waitKey(0) & 0xFF == ord('q')