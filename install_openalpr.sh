sudo apt-get install --assume-yes libpng12-dev libjpeg62-dev libtiff4-dev zlib1g-dev
sudo apt-get install --assume-yes build-essential
sudo apt-get install --assume-yes autoconf automake libtool
sudo apt-get install --assume-yes git-core
sudo apt-get install --assume-yes cmake
sudo mkdir /usr/local/src/openalpr/
sudo chmod -R  777 /usr/local/src/openalpr/
cd /usr/local/src/openalpr/
git clone --recursive https://github.com/DanBloomberg/leptonica

wget https://github.com/tesseract-ocr/tesseract/archive/3.02.02.tar.gz
wget https://sourceforge.net/projects/tesseract-ocr-alt/files/tesseract-ocr-3.02.eng.tar.gz

tar xf /usr/local/src/openalpr/tesseract-ocr-3.02.02.tar.gz
tar xf /usr/local/src/openalpr/tesseract-ocr-3.02.eng.tar.gz

cd leptonica
./configure --prefix=/usr/local

make
make install

cd /usr/local/src/openalpr/tesseract-ocr/
./autogen.sh
./configure
make
sudo make install
sudo ldconfig

cd /usr/local/src/openalpr/

git clone https://github.com/openalpr/openalpr.git

cd /usr/local/src/openalpr/openalpr/src

cmake ./
make
sudo make install

cd  /usr/local/src/openalpr/openalpr/src/bindings/python/

sudo python setup.py install
sudo python3 setup.py install
