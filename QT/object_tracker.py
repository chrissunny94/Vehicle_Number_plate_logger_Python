import cv2
import sys
from hog_detector import detect_car
from cloudAPI import return_info2
import argparse
import imutils
from camera import VideoCamera
(major_ver, minor_ver, subminor_ver) = (cv2.__version__).split('.')


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


def object_tracker(frame , bbox):
	# Set up tracker.
    # Instead of MIL, you can also use
 
    tracker_types = ['BOOSTING', 'MIL','KCF', 'TLD', 'MEDIANFLOW', 'GOTURN']
    tracker_type = tracker_types[2]
 
    if int(minor_ver) < 3:
        tracker = cv2.Tracker_create(tracker_type)
    else:
        if tracker_type == 'BOOSTING':
            tracker = cv2.TrackerBoosting_create()
        if tracker_type == 'MIL':
            tracker = cv2.TrackerMIL_create()
        if tracker_type == 'KCF':
            tracker = cv2.TrackerKCF_create()
        if tracker_type == 'TLD':
            tracker = cv2.TrackerTLD_create()
        if tracker_type == 'MEDIANFLOW':
            tracker = cv2.TrackerMedianFlow_create()
        if tracker_type == 'GOTURN':
            tracker = cv2.TrackerGOTURN_create()
    ok = tracker.init(frame, bbox)
    	
    while ok:
        # Read a new frame
	#print "tracker started"
        frame = video_camera.get_frame()
        
         
        # Start timer
        timer = cv2.getTickCount()
 
        # Update tracker
        ok, bbox = tracker.update(frame)
 
        # Calculate Frames per second (FPS)
        fps = cv2.getTickFrequency() / (cv2.getTickCount() - timer);
 
        # Draw bounding box
        if ok:
            # Tracking success
            p1 = (int(bbox[0]), int(bbox[1]))
            p2 = (int(bbox[0] + bbox[2]), int(bbox[1] + bbox[3]))
            cv2.rectangle(frame, p1, p2, (255,0,0), 2, 1)
        else :
            # Tracking failure
            cv2.putText(frame, "Tracking failure detected", (100,80), cv2.FONT_HERSHEY_SIMPLEX, 0.75,(0,0,255),2)
	    break	
 
        # Display tracker type on frame
        cv2.putText(frame, tracker_type + " Tracker", (100,20), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (50,170,50),2);
     
        # Display FPS on frame
        cv2.putText(frame, "FPS : " + str(int(fps)), (100,50), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (50,170,50), 2);
 
        # Display result
        cv2.imshow("Tracking", frame)
 
        # Exit if ESC pressed
        key = cv2.waitKey(1) & 0xff
        if key == ord("q"):
			break
    cv2.destroyAllWindows()	

if __name__ == '__main__' :
    
    while True:	
    	
 
    	frame = video_camera.get_frame()
	cv2.imshow("input", frame)
    	
	key = cv2.waitKey(1) & 0xff
        
	if key == ord("q"):
			break
	#checking for hog response
    	ok,hog_out , bbox = detect_car(frame)
    	if ok:
    		#print bbox
		plate , confidence,colour , make , body_type , year ,make_model , number_plate = return_info2(frame)
		print plate , confidence,colour , make , body_type , year ,make_model		
    		object_tracker(frame,bbox)
	
