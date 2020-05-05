# -*- coding: utf-8 -*-

__author__      = "Chris Sunny Thaliyath"
__copyright__   = "Copyright 2018, advancedcv.github.io"
__version__ = "0.1"
__license__ = "GPL"


from PyQt4 import QtCore, QtGui, uic
from PyQt4.QtCore import *
from PyQt4.QtGui import *
import sys
import cv2
import numpy as np
import threading
import time
import Queue
from hog_detector import detect_car
from camera import VideoCamera , IPCamera
import argparse
import imutils
import cv2
from read_number_plate import *
import dlib
from Openalpr import read_number_plate
import time 
last_time = time.time() - 5


#load car detector
detector = dlib.fhog_object_detector("../DATA/SVM/car_detector.svm")
win = dlib.image_window()

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



running = False
capture_thread = None
form_class = uic.loadUiType("../DATA/UI/simple.ui")[0]
q = Queue.Queue()
frame = {}
 
# captures the image and puts it into a queue
def grab(cam, queue, width, height, fps):
    global running
    

    while running:
       
        frame = video_camera.get_frame()
       
        if queue.qsize() < 10:
            queue.put(frame)
        else:
            #print queue.qsize()
            pass



#UI class
class OwnImageWidget(QtGui.QWidget):
    def __init__(self, parent=None):
        super(OwnImageWidget, self).__init__(parent)
        self.image = None

    def setImage(self, image):
        self.image = image
        sz = image.size()
        self.setMinimumSize(sz)
        self.update()

    def paintEvent(self, event):
        qp = QtGui.QPainter()
        qp.begin(self)
        if self.image:
            qp.drawImage(QtCore.QPoint(0, 0), self.image)
        qp.end()



class MyWindowClass(QtGui.QMainWindow, form_class):
    def __init__(self, parent=None ):
        QtGui.QMainWindow.__init__(self, parent)
        self.setupUi(self)
	
	#super(Form,self).__init__(parent)
	
        self.carLog = QListWidget(self.carLog)
        

        self.startButton.clicked.connect(self.start_clicked)
        self.stopButton.clicked.connect(self.stop_clicked)

        self.window_width = self.input.frameSize().width()
        self.window_height = self.input.frameSize().height()
        self.input = OwnImageWidget(self.input)
        self.detectedcar = OwnImageWidget(self.detectedcar)
        self.numberplate = OwnImageWidget(self.numberplate)         

        self.timer = QtCore.QTimer(self)
        self.timer.timeout.connect(self.update_frame)
        self.timer.start(.1)
        self.last_time = time.time()


    def start_clicked(self):
        global running
        #running = True
        
        #self.startButton.setEnabled(False)
        if not running:
            running = True
            self.startButton.setText('Stop')
            capture_thread.start()
        else:
            running = False
            self.startButton.setText('Stop')
            capture_thread.terminate()

    def stop_clicked(self):
        global running
        running = False
        capture_thread.stop()
        self.stopButton.setEnabled(False)
        self.stopButton.setText('Starting...')
    
    
    def Add(self):

        self.text,ok = QInputDialog.getText(self,'Input Dialog','Enter Value')

        if ok:
                  print self.text  
                  self.qListWidget.addItem(self.text)


    def Remove(self):
        row = self.qListWidget.currentRow()
        item = self.qListWidget.takeItem(row)
        del item
            
    
    def Edit(self):
        
        text_replace,ok = QInputDialog.getText(self,'Input Dialog','Enter Value')
        current_item_row = self.qListWidget.currentRow()
        current_item_text = self.qListWidget.item(current_item_row)
        current_item_text.setText(text_replace)




    def Up(self):
       
        current_item_row = self.qListWidget.currentRow()
        if current_item_row > 0:
            current_item_text = self.qListWidget.item(current_item_row)
            print str(current_item_text.text())

            up_item_row = current_item_row - 1
            up_item_text = self.qListWidget.item(up_item_row)
            print str(up_item_text.text())

            self.qListWidget.takeItem(current_item_row)
            self.qListWidget.insertItem(current_item_row,up_item_text.text())
            self.qListWidget.takeItem(up_item_row)
            self.qListWidget.insertItem(up_item_row,current_item_text.text())
        else:
              print "Already at top of list."

    def Sort(self):
        self.qListWidget.sortItems()


    def reject(self):
        self.accept()

    def accept(self):
        QDialog.done(self,0)
	
    # This is the function where the UI updates the frames 	
    def update_frame(self):
        global q
        if not q.empty():
            #self.startButton.setText('Camera is live')
            frame = q.get()
            img = frame

            img_height, img_width, img_colors = img.shape
            scale_w = float(self.window_width) / float(img_width)
            scale_h = float(self.window_height) / float(img_height)
            scale = min([scale_w, scale_h])

            if scale == 0:
                scale = 1
            
            img = cv2.resize(img, None, fx=scale, fy=scale, interpolation = cv2.INTER_CUBIC)
            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            height, width, bpc = img.shape
            bpl = bpc * width
            image = QtGui.QImage(img.data, width, height, bpl, QtGui.QImage.Format_RGB888)
            self.input.setImage(image)




            try:
		ok,output , bbox = detect_car(frame)
                
                #output = frame
                #cv2.imshow("output",output)
                output_height, output_width, output_colors = output.shape
                output_scale_w = float(self.window_width) / float(output_width)
                output_scale_h = float(self.window_height) / float(output_height)
                output_scale = min([output_scale_w, output_scale_h])

                if output_scale == 0:
                    output_scale = 1
            
                output = cv2.resize(output, None, fx=output_scale, fy=output_scale, interpolation = cv2.INTER_CUBIC)
                output = cv2.cvtColor(output, cv2.COLOR_BGR2RGB)
                output_height, output_width, output_bpc = output.shape
                output_bpl = output_bpc * output_width
                output_image = QtGui.QImage(output.data, output_width, output_height, output_bpl, QtGui.QImage.Format_RGB888)
                self.detectedcar.setImage(output_image)
            except:
                print "car_detector failed"

            

            try:
                
                numberplate,confidence,output = (read_number_plate(frame))
                output = cv2.resize(output, None, fx=1, fy=1, interpolation = cv2.INTER_CUBIC)
                output = cv2.cvtColor(output, cv2.COLOR_BGR2RGB)
                output_height, output_width, output_bpc = output.shape
                output_bpl = output_bpc * output_width
                output_image = QtGui.QImage(output.data, output_width, output_height, output_bpl, QtGui.QImage.Format_RGB888)
                self.numberplate.setImage(output_image)
                now = time.time()
                
                if (now - self.last_time > 2):
                    
                    self.carLog.addItems([(numberplate)])
                    self.last_time = now
            except:
                print "numberplate detector falied"
            
            
            

    def closeEvent(self, event):
        global running
        running = False



capture_thread = threading.Thread(target=grab, args = (0, q, 1920, 1080, 30))



app = QtGui.QApplication(sys.argv)
w = MyWindowClass(None )
w.setWindowTitle('Vehicle_Number_plate_logger')
w.show()


#form.show()
app.exec_()


