# Vehicle Counting + Number Plate Reader using OpenCv

### Modules used
- OpenCV
- tesseracact OCR
- QT for UI
- dlib 
- openalpr
### Individual Scripts

- **main.py**
This is the script to see everything running without UI 

- **carDetect.py**
This script contains the class for detecting the car using HaarCascade

- **hog_detector.py**
This script contains the class for detecting the car using HOG method (SVM)

- **object_tracker.py**
This script contains the class for tracking the detected car from HOG method .(This can be used to count the cars)


- **readnumberplat.py**
This script contains the functions to convert the image into text using Tesseract 

- **Openalpr.py**
This script contains the functions to read the numberplate using OpenAlpr library 

- **cloudAPI.py**
This script contains the functions to read the numberplate using OpenAlpr library from the cloud server


- **start_UI.py**
This script starts the QT based UI
 
## Instructions 

You can run all the scripts using the below method . All the scripts can be tested individually .

***With UI***

	python start_UI.py  -v XXX
	

***HOG detector for car***

	python hog_detector.py -v XXX

***OpenALPR number plate reader***
	
	python Openalpr.py -v ../../IM*	
	
***Without UI***
	
	python main.py  -v  XXX
	
**what are the parameters**
XXX

for webcam
	
	-v 0
	
for video(example)

	-v IMG_6.MOV
	





**Screenshot**

![](../docs/qt.png) 
