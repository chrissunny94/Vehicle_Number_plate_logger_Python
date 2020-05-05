sudo apt-get install --assume-yes libpng12-dev libjpeg62-dev libtiff4-dev zlib1g-dev
sudo apt-get install --assume-yes build-essential
sudo apt-get install --assume-yes autoconf automake libtool
sudo apt-get install --assume-yes git-core
sudo apt-get install --assume-yes cmake

# Install prerequisites
sudo apt-get install libopencv-dev libtesseract-dev git cmake build-essential libleptonica-dev
sudo apt-get install liblog4cplus-dev libcurl3-dev

# If using the daemon, install beanstalkd
sudo apt-get install beanstalkd

cd 
# Clone the latest code from GitHub
git clone https://github.com/openalpr/openalpr.git

# Setup the build directory
cd openalpr/src
mkdir build
cd build

# setup the compile environment
cmake -DCMAKE_INSTALL_PREFIX:PATH=/usr -DCMAKE_INSTALL_SYSCONFDIR:PATH=/etc ..

# compile the library
make

# Install the binaries/libraries to your local system (prefix is /usr)
sudo make install
sudo apt-get install python-qt4
