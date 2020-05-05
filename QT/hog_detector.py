import dlib
import sys
import cv2
import argparse
import imutils
from camera import VideoCamera
from skimage import io





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



## This is the main function for detecting the car using the HOG method
def detect_car(frame):
	#load car detector
	detector = dlib.fhog_object_detector("../DATA/SVM/car_detector.svm")
	#win = dlib.image_window()
	try:
		dets = detector(frame)
		for d in dets:
			frame = frame[int(d.top()):int(d.bottom()+20),int(d.left()): int(d.right()+20)]
			 # Display the resulting frame
			cv2.imshow("frame",frame)
		return True ,frame ,(int(d.left()) ,int(d.top()),int(d.right()+20-d.left()) ,int(d.bottom()+20-d.top()))
			
	except:
		#print "HOG detector failed"
		return False, None , None

if __name__ == '__main__':
	
	while True:
		frame = video_camera.get_frame()
		try:
			cv2.imshow("input",frame)
		except:
			print "failed"
		status , output , bbox = detect_car(frame)
		print status , bbox
		if status:
			cv2.imshow("HOGoutput", output)
		key = cv2.waitKey(1) & 0xFF

		# if the 'q' key is pressed, stop the loop
		if key == ord("q"):
			break
