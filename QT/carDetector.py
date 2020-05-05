from collections import deque
import numpy as np
import argparse
import imutils
import cv2
from matplotlib import pyplot as plt
import numpy as np
import cv2
from copy import deepcopy
from PIL import Image
import pytesseract as tess
from camera import VideoCamera

# This is a haar cascade method of classification 
# construct the argument parse and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-v", "--video",
    help="path to the (optional) video file")
ap.add_argument("-b", "--buffer", type=int, default=64,
    help="max buffer size")
ap.add_argument("-m", "--model",
    help="path to trained model")
args = vars(ap.parse_args())


if not args.get("video", False):
    video_camera = VideoCamera(0)
    # otherwise, grab a reference to the video file
else:
    video_camera = VideoCamera(args["video"])



# This is a simple Haar cascade method to detect cars

class carDetector(object):
	"""docstring for carDetector"""
	def __init__(self):
		#Code for car detector
		self.car_cascade = cv2.CascadeClassifier('../DATA/cascades/cars.xml')
		self.frame = None
		self.detected_car = None
	def update_frame(self,frame):
		self.frame = frame
	def get_frame(self):
		return self.frame

	def detect_car(self):
		frame = self.frame
		gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
			
		cars = []
		ncars = 0
		cars = self.car_cascade.detectMultiScale(gray, 1.4, 6)
		
		for (x, y, w, h) in cars:
			cv2.rectangle(frame, (x,y), (x+w,y+h), (0,0,255), 2)
			ncars = ncars + 1
			self.detected_car = frame[y:y+h, x:x+w]
			
			
	def get_detected_car(self):
		
		return self.detected_car

car_detect = carDetector()
if __name__ == '__main__':
	
	while True:
		frame = video_camera.get_frame()
		try:
			cv2.imshow("input",frame)
		except:
			print "failed"
		car_detect.update_frame(frame)
		car_detect.detect_car()
		output = car_detect.get_detected_car()
		cv2.imshow("output", output)

		key = cv2.waitKey(1) & 0xFF

		# if the 'q' key is pressed, stop the loop
		if key == ord("q"):
			break

	
