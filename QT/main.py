from carDetector import carDetector
from camera import VideoCamera , IPCamera
import argparse
import imutils
import cv2
from read_number_plate import *
from pyANPD import *
import dlib
import threading
import os
#import detect

# construct the argument parse and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-v", "--video",
    help="path to the (optional) video file")
ap.add_argument("-b", "--buffer", type=int, default=64,
    help="max buffer size")
ap.add_argument("-m", "--model",
    help="path to trained model")
args = vars(ap.parse_args())



#load car detector
detector = dlib.fhog_object_detector("../DATA/SVM/car_detector.svm")
win = dlib.image_window()

if not args.get("video", False):
    video_camera = VideoCamera(0)
    # otherwise, grab a reference to the video file
else:
    video_camera = VideoCamera(args["video"])


car_detector = carDetector()    




# This function detects the number plate
def detect_numberplate(im):
	im_gray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY) / 255.
	cv2.imshow("Input for deep leanring" , im)
	#Loading the model
    	f = numpy.load(args["model"])
    	param_vals = [f[n] for n in sorted(f.files, key=lambda s: int(s[4:]))]
    	print ("RUN")

    	for pt1, pt2, present_prob, letter_probs in post_process(
                                                  detect(im_gray, param_vals)):
        	pt1 = tuple(reversed(map(int, pt1)))
        	pt2 = tuple(reversed(map(int, pt2)))

        	code = letter_probs_to_code(letter_probs)

        	color = (0.0, 255.0, 0.0)
        	cv2.rectangle(im, pt1, pt2, color)

        	cv2.putText(im,
                    code,
                    pt1,
                    cv2.FONT_HERSHEY_PLAIN,
                    1.5,
                    (0, 0, 0),
                    thickness=5)

        	cv2.putText(im,
                    code,
                    pt1,
                    cv2.FONT_HERSHEY_PLAIN,
                    1.5,
                    (255, 255, 255),
                    thickness=2)

    	cv2.imshow("output",im)
    	
	return im ,code

# this is the main loop
def loop():
	frame = video_camera.get_frame()
	try:
		cv2.imshow("input",frame)
	except:
		print "failed"	
	try:
		dets = detector(frame)
		for d in dets:
			cv2.rectangle(frame, (d.left(), d.top()), (d.right(), d.bottom()), (0, 0, 255), 2)
			print (int(d.left()), int(d.top()) ), (int(d.right()), int(d.bottom()) )
		frame = frame[int(d.top()):int(d.bottom()+20),int(d.left()): int(d.right()+20)]
		cv2.imshow("HOG output",frame)
		try:
			
			detect_numberplate(frame)
		except:
			print("Deep learning failed ")
		
		
		try: 
			output = process_image(frame, 0, type='rect')
			cv2.imshow("Detected Number plate",output)
			try:
				threshold_img = preprocess(output)
				contours= extract_contours(threshold_img)
				cleanAndRead(car_detector.get_detected_car(),contours)

			except:
				print "Number plate reader failed"
		except:
			print "Plate detector failed"
			
			
	except:
		print "HOG detector failed"
	

	try:
		dets = detector(frame)
		for d in dets:
			cv2.rectangle(frame, (d.left(), d.top()), (d.right(), d.bottom()), (0, 0, 255), 2)
			print (int(d.left()), int(d.top()) ), (int(d.right()), int(d.bottom()) )
		frame = frame[int(d.top()):int(d.bottom()),int(d.left()): int(d.right())]
		cv2.imshow("HOG output",frame)
		try: 
			output = process_image(frame, 0, type='rect')
			cv2.imshow("Detected Number plate",output)
			try:
				threshold_img = preprocess(output)
				contours= extract_contours(threshold_img)
				cleanAndRead(car_detector.get_detected_car(),contours)

			except:
				print "Number plate reader failed"
		except:
			print "Plate detector failed"
			
			
	except:
		print "HOG detector failed"

     	
	

if __name__ == '__main__':
	
	while True:
		loop()
		key = cv2.waitKey(1) & 0xFF

		# if the 'q' key is pressed, stop the loop
		if key == ord("q"):
			break
