import cv2
from matplotlib import pyplot as plt
img = cv2.imread("/home/light/Desktop/2015-10-16-151953.jpg",0)
equ = cv2.equalizeHist(img)
sobelx = cv2.Sobel(equ,cv2.CV_64F,1,0,ksize=5)
plt.imshow(sobelx,cmap='gray')
plt.show()
