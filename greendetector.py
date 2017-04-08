import cv2
import numpy as np
import picamera
from picamera import PiCamera
from picamera.array import PiRGBArray

h = 320
w = 240
points = []
kernel = np.ones((3,3),np.uint8)
model = np.zeros((100,100))
model[48:52,48:52] = 1
camera = PiCamera()
camera.resolution = (h,w)
camera.framerate = 30
rawCapture = PiRGBArray(camera,size=(h,w))

###UI trackbars for HSV threshold values
def nothing(x):
	pass
cv2.namedWindow('img',0)
cv2.createTrackbar('HUE','img',0,255,nothing)
cv2.createTrackbar('SAT','img',0,255,nothing)
cv2.createTrackbar('VAL','img',0,255,nothing)
cv2.resizeWindow('img',640,480)
lb = np.array([45,75,75])
ub = np.array([70,255,255])

def bounds():
	hue = cv2.getTrackbarPos('HUE','img')
	sat = cv2.getTrackbarPos('SAT','img') 
	val = cv2.getTrackbarPos('VAL','img') 

	lb = np.array([(hue-20),sat,val])
	ub = np.array([(hue+20),255,255])

	#lb = np.array([45,75,75])
	#ub = np.array([70,255,255])
	return lb, ub


for frame in camera.capture_continuous(rawCapture, format='bgr',use_video_port=True):
	frame = frame.array

	###get frame and convert to HSV space
	hsv = cv2.cvtColor(frame,cv2.COLOR_BGR2HSV)

	lb,ub = bounds()
	green = cv2.inRange(hsv, lb,ub)
	green = cv2.morphologyEx(green, cv2.MORPH_OPEN, kernel)
	img = cv2.GaussianBlur(green,(5,5),0)    
	
	edges = cv2.Canny(img,150,200)
	#corners = cv2.cornerHarris(edges,5,5,.1)    
	corners = cv2.goodFeaturesToTrack(edges,4,0.01,100)
	if corners is not None:
		corners = np.int0(corners)
		#print corners.ndim
		#print "\n"
		for i in corners:
		    x,y = i.ravel()
		    cv2.circle(frame,(x,y),10,(255,0,255),-1)

	#open = cv2.morphologyEx(corners, cv2.MORPH_OPEN, kernel)
	#cv2.circle(frame,(200,100),10,(255,0,255),-1)
	green = cv2.cvtColor(green,cv2.COLOR_GRAY2BGR)
	edges = cv2.cvtColor(edges,cv2.COLOR_GRAY2BGR)
	final = np.concatenate((frame, hsv, green),axis=1)


	cv2.imshow('img',final)
	cv2.moveWindow('img',0,0)
	key = cv2.waitKey(1) & 0xFF
	rawCapture.truncate(0)
	if key == ord('q'):
		break
