from openalpr import Alpr
import sys
import cv2
import argparse
import imutils
from camera import VideoCamera
from hog_detector import detect_car
import dlib

from carDetector import *
car_detect = carDetector()

#load car detector
detector = dlib.fhog_object_detector("../DATA/SVM/car_detector.svm")
win = dlib.image_window()

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


def read_number_plate(im):
	#initialize the openalpr class instance 
	alpr = Alpr("us", "../DATA/runtime_data/config/us.conf", "../DATA/runtime_data")
	if not alpr.is_loaded():
    		print("Error loading OpenALPR")
    		sys.exit(1)

	alpr.set_top_n(20)
	alpr.set_default_region("ca")
	results = alpr.recognize_ndarray(im)
	i = 0
	# extracting the json files
	plate = results['results'][0]
	candidate = plate['candidates'][0]
	plate_coordinates = results['results'][0]['coordinates']	
	
	alpr.unload()
	out = im[plate_coordinates[0]['y']:plate_coordinates[2]['y']+20, plate_coordinates[0]['x']:plate_coordinates[1]['x']+20]
	return candidate['plate'] , candidate['confidence'] , out


if __name__ == '__main__':
	
	while True:
		frame = video_camera.get_frame()
		
		try:
			cv2.imshow("input",frame)
			# The input is fed into the detect_car function which is inside the hog_detector
			try:
				status = False
				#status,output_hog,bbox = detect_car(frame)
				#Hog returns the status , cropped out image , bounding box
				car_detect.update_frame(frame)
				car_detect.detect_car()
				output = car_detect.get_detected_car()
				cv2.imshow("Hog", output) 
				#print status , bbox
				if True:
					plate,confidence,out = read_number_plate(frame)
					print plate , confidence
					cv2.imshow("cropped plate",out)
					
			
			except:
				pass
		except:
			pass

		
		key = cv2.waitKey(1) & 0xFF

		# if the 'q' key is pressed, stop the loop
		if key == ord("q"):
			break
		
