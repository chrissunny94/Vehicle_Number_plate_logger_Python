#!/usr/bin/python

import requests
import base64
import json
import dlib
from carDetector import carDetector
from camera import VideoCamera , IPCamera
import argparse
import imutils
import cv2

# Sample image file is available at http://plates.openalpr.com/ea7the.jpg
IMAGE_PATH = 'frame.jpg'



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


car_detector = carDetector()  
detector = dlib.fhog_object_detector("../DATA/SVM/car_detector.svm")
win = dlib.image_window()




# We basically encode the image in 64 bit manner and send it over to the OpenAlpr cloud API
def return_info(frame):
	SECRET_KEY = 'sk_df1b80fc1591519b091f2726'
	try:
                dets = detector(frame)
                for d in dets:
                    cv2.rectangle(frame, (d.left(), d.top()), (d.right(), d.bottom()), (0, 0, 255), 2)
                    #print (int(d.left()), int(d.top()) ), (int(d.right()), int(d.bottom()) )
                    frame = frame[int(d.top()):int(d.bottom()+20),int(d.left()): int(d.right()+20)]
                cv2.imshow("HOG output",frame)
                
		cv2.imwrite("frame.jpg",frame)
		with open(IMAGE_PATH, 'rb') as image_file:
    			img_base64 = base64.b64encode(image_file.read())
		url = 'https://api.openalpr.com/v2/recognize_bytes?recognize_vehicle=1&country=us&secret_key=%s' % (SECRET_KEY)
		r = requests.post(url, data = img_base64)
		
		#print(json.dumps(r.json(), indent=2))
		
		plate = r.json()['results'][0]['plate']
		
		confidence = r.json()['results'][0]['confidence']
		
		plate_coordinates = r.json()['results'][0]['coordinates']
		vehicle_colour = r.json()['results'][0]['vehicle']['color'][0]['name']
		vehicle_make = r.json()['results'][0]['vehicle']['make'][0]['name']
		vehicle_body_type = r.json()['results'][0]['vehicle']['body_type'][0]['name']
		vehicle_year = r.json()['results'][0]['vehicle']['year'][0]['name']
		vehicle_make_model = r.json()['results'][0]['vehicle']['make_model'][0]['name']
		im = frame[plate_coordinates[0]['y']:plate_coordinates[2]['y']+20, plate_coordinates[0]['x']:plate_coordinates[1]['x']+20]
		return plate , confidence , vehicle_colour , vehicle_make, vehicle_body_type, vehicle_year , vehicle_make_model , im
	except:
		print "HOG detector failed"
	
	return 0 , 0, 0 ,0,0,0,0,0

def return_info2(frame):
	SECRET_KEY = 'sk_df1b80fc1591519b091f2726'
	try:
                
                
		cv2.imwrite("frame.jpg",frame)
		with open(IMAGE_PATH, 'rb') as image_file:
    			img_base64 = base64.b64encode(image_file.read())
		url = 'https://api.openalpr.com/v2/recognize_bytes?recognize_vehicle=1&country=us&secret_key=%s' % (SECRET_KEY)
		r = requests.post(url, data = img_base64)
		
		#print(json.dumps(r.json(), indent=2))
		
		plate = r.json()['results'][0]['plate']
		
		confidence = r.json()['results'][0]['confidence']
		
		plate_coordinates = r.json()['results'][0]['coordinates']
		vehicle_colour = r.json()['results'][0]['vehicle']['color'][0]['name']
		vehicle_make = r.json()['results'][0]['vehicle']['make'][0]['name']
		vehicle_body_type = r.json()['results'][0]['vehicle']['body_type'][0]['name']
		vehicle_year = r.json()['results'][0]['vehicle']['year'][0]['name']
		vehicle_make_model = r.json()['results'][0]['vehicle']['make_model'][0]['name']
		im = frame[plate_coordinates[0]['y']:plate_coordinates[2]['y']+20, plate_coordinates[0]['x']:plate_coordinates[1]['x']+20]
		return plate , confidence , vehicle_colour , vehicle_make, vehicle_body_type, vehicle_year , vehicle_make_model , im
	except:
		print "HOG detector failed"
	
	return 0 , 0, 0 ,0,0,0,0,0

if __name__ == '__main__':
	
	while True:
		frame = video_camera.get_frame()
		try:
			cv2.imshow("input",frame)
		except:
			print "failed"	
		plate , confidence,colour , make , body_type , year ,make_model , number_plate = return_info(frame)
		print plate , confidence,colour , make , body_type , year ,make_model
		cv2.imshow("number_plate",number_plate)
		key = cv2.waitKey(1) & 0xFF

		# if the 'q' key is pressed, stop the loop
		if key == ord("q"):
			break
