from flask import Flask, render_template, Response, jsonify, request
from camera import VideoCamera , IPCamera
from carDetector import carDetector
import cv2
import argparse
import imutils
from flask import g

# construct the argument parse and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-v", "--video",
    help="path to the (optional) video file")
ap.add_argument("-b", "--buffer", type=int, default=64,
    help="max buffer size")
args = vars(ap.parse_args())

if not args.get("video", False):
    video_camera = VideoCamera(0)
    

# otherwise, grab a reference to the video file
else:
    video_camera = VideoCamera(args["video"])
    

app = Flask(__name__)

#video_camera = IPCamera()

global_frame = None
frame = None
car_detector = carDetector()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/record_status', methods=['POST'])
def record_status():
    global video_camera 
    if video_camera == None:
        video_camera = VideoCamera()

    json = request.get_json()

    status = json['status']

    if status == "true":
        video_camera.start_record()
        return jsonify(result="started")
    else:
        video_camera.stop_record()
        return jsonify(result="stopped")

def video_stream(car_detector):
    global video_camera 
    global global_frame
   
    #global car_detector
    if video_camera == None:
        video_camera = VideoCamera()
        
    while True:
        frame = video_camera.get_frame()
        car_detector.update_frame(frame)

        try:
            output = car_detector.detect_car()
            
        except:
            print "car_detector failed"
           
       
        ret, jpeg = cv2.imencode('.jpg', car_detector.get_frame())
        jpeg = jpeg.tobytes()    
        
        if jpeg != None:
            global_frame = frame
            yield (b'--frame\r\n'
                    b'Content-Type: image/jpeg\r\n\r\n' + jpeg + b'\r\n\r\n')
        else:
            yield (b'--frame\r\n'
                            b'Content-Type: image/jpeg\r\n\r\n' + global_frame + b'\r\n\r\n')

            
def car_stream(car_detector):
    
    
    while True:
        out_jpeg = None
        print "\n\nFRAME", car_detector.get_detected_car()
        ret, out_jpeg = cv2.imencode('.jpg', car_detector.get_detected_car())
        out_jpeg = out_jpeg.tobytes()  
        
           
        if out_jpeg != None:
            
            yield (b'--frame\r\n'
                    b'Content-Type: image/jpeg\r\n\r\n' + out_jpeg + b'\r\n\r\n')
       


@app.route('/video_viewer')
def video_viewer():
    return Response(video_stream(car_detector),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/processed_video')
def processed_video():
    return Response(car_stream(car_detector),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    app.run(host='0.0.0.0', threaded=True)
