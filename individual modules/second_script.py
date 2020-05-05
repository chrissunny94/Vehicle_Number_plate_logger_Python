# USAGE
# python base_script.py --video *.mp4
# python base_script.py

# import the necessary packages
from collections import deque
import numpy as np
import argparse
import imutils
import cv2
from matplotlib import pyplot as plt

#Code for car detector
car_cascade = cv2.CascadeClassifier('cascades/cars.xml')

# construct the argument parse and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-v", "--video",
	help="path to the (optional) video file")
ap.add_argument("-b", "--buffer", type=int, default=64,
	help="max buffer size")
args = vars(ap.parse_args())

# if a video path was not supplied, grab the reference
# to the webcam
if not args.get("video", False):
	camera = cv2.VideoCapture(0)

# otherwise, grab a reference to the video file
else:
	camera = cv2.VideoCapture(args["video"])

# keep looping
while True:
	# grab the current frame
	(grabbed, frame) = camera.read()

	# if we are viewing a video and we did not grab a frame,
	# then we have reached the end of the video
	if args.get("video") and not grabbed:
		break

	cv2.imshow("Frame", frame)
	gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
	# Detect cars
	cars = []
	ncars = 0
	try:
		cars = car_cascade.detectMultiScale(gray, 1.4, 6)
	except:
		print("Car detector failed")
	# Draw border
	for (x, y, w, h) in cars:
		cv2.rectangle(frame, (x,y), (x+w,y+h), (0,0,255), 2)
		ncars = ncars + 1
		cv2.imshow("Detected cars", frame)
	# Show image
	#plt.figure(figsize=(10,20))
	#plt.imshow(frame)
	
	key = cv2.waitKey(1) & 0xFF

	# if the 'q' key is pressed, stop the loop
	if key == ord("q"):
		break
# cleanup the camera and close any open windows
camera.release()
cv2.destroyAllWindows()
