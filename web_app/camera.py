import cv2
import threading
import urllib2
import numpy as np
import sys



class RecordingThread (threading.Thread):
    def __init__(self, name, camera):
        threading.Thread.__init__(self)
        self.name = name
        self.isRunning = True

        self.cap = camera
        fourcc = cv2.VideoWriter_fourcc(*'MJPG')
        self.out = cv2.VideoWriter('./static/video.avi',fourcc, 20.0, (640,480))

    def run(self):
        while self.isRunning:
            ret, frame = self.cap.read()
            if ret:
                self.out.write(frame)

        self.out.release()

    def stop(self):
        self.isRunning = False

    def __del__(self):
        self.out.release()

class VideoCamera(object):
    def __init__(self,argument):
        # Open a camera
        self.cap = cv2.VideoCapture(argument)
        #self.cap = cv2.VideoCapture('192.168.43.1:8080/video')
        
        # Initialize video recording environment
        self.is_record = False
        self.out = None

        # Thread for recording
        self.recordingThread = None
    
    def __del__(self):
        self.cap.release()
    
    def get_frame(self):
        ret, frame = self.cap.read()

        if ret:
            
            return frame
      
        else:
            return None

    def start_record(self):
        self.is_record = True
        self.recordingThread = RecordingThread("Video Recording Thread", self.cap)
        self.recordingThread.start()

    def stop_record(self):
        self.is_record = False

        if self.recordingThread != None:
            self.recordingThread.stop()

class IPCamera(object):
    def __init__(self):
        # Open a camera
        self.host = "192.168.43.1:8080"
        self.hoststr = 'http://' + self.host + '/video'
        print 'Streaming ' + self.hoststr

        self.stream=urllib2.urlopen(self.hoststr)

        
        
        # Initialize video recording environment
        self.is_record = False
        self.out = None
        self.bytes = ''

        # Thread for recording
        self.recordingThread = None
    
    def __del__(self):
        self.cap.release()
    
    def get_frame(self):
        
        self.bytes+=self.stream.read(1024)
        a = self.bytes.find('\xff\xd8')
        print a ,"AAAA"
        b = self.bytes.find('\xff\xd9')
        print b ,"BBB"
        ret = False
        if a!=-1 and b!=-1:
            jpg = self.bytes[a:b+2]
            self.bytes= self.bytes[b+2:]
            frame = cv2.imdecode(np.fromstring(jpg, dtype=np.uint8),1)
            cv2.imshow("IPCAME",frame)
            if cv2.waitKey(1) ==27:
                exit(0)

            ret = True
        


        if ret:
            #ret, jpeg = cv2.imencode('.jpg', frame)

            # Record video
            # if self.is_record:
            #     if self.out == None:
            #         fourcc = cv2.VideoWriter_fourcc(*'MJPG')
            #         self.out = cv2.VideoWriter('./static/video.avi',fourcc, 20.0, (640,480))
                
            #     ret, frame = self.cap.read()
            #     if ret:
            #         self.out.write(frame)
            # else:
            #     if self.out != None:
            #         self.out.release()
            #         self.out = None  

            #return jpeg.tobytes()
            return frame
      
        else:
            return None

    def start_record(self):
        self.is_record = True
        #self.recordingThread = RecordingThread("Video Recording Thread", self.stream)
        #self.recordingThread.start()

    def stop_record(self):
        self.is_record = False

        if self.recordingThread != None:
            self.recordingThread.stop()
   
