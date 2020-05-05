## Folder contents

- **QT**
This folder contains the QT based UI scripts *(Complete)*

- **WebApp**
This folder contains the Flask Based WebUI *(Incomplete)*

- **Underwork**
This is an improved version of the number plate detector *(Complete)*

- **Individual Modules**
This folder contains the individual Python Scripts for easy inspection analysis  

- **DATA**
This folder contains the 

1) UI (For QT)

2) Haar Cascades for Detecting car

3) testData , images of cars

4) characters , for training on letters


## Future improvements

- Use of Neural Networks for OCR and Car detection


## Clone the repository
	cd 
	git clone https://github.com/advancedCV/vehicle_numberplate_logger
	cd vehicle_numberplate_logger
	
## install instruction
	
	sudo apt-get update
	sudo apt-get -f install
	sudo apt-get dist-upgrade
	sudo apt-get upgrade
	./install_dependencies.sh

	sudo apt-get install python-qt4
	sudo apt-get install python-pyqt5

## To install spyder 
	sudo apt-get install spyder*


## To install opencv

	./install_opencv.sh

## To install OpenAlpr

	./install_openalpr.sh

## fix virtualbox

	sudo mount /dev/cdrom /mnt
	cd /mnt
	sudo dnf install -y dkms kernel-devel kernel-devel-$(uname -r)
	sudo su
	./VBoxLinuxAdditions.run

