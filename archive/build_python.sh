VERSION=3.7.15
#sudo apt-get update -y
#sudo apt-get install build-essential tk-dev libncurses5-dev libncursesw5-dev libreadline6-dev libdb5.3-dev libgdbm-dev libsqlite3-dev libssl-dev libbz2-dev libexpat1-dev liblzma-dev zlib1g-dev libffi-dev -y
wget https://www.python.org/ftp/python/${VERSION}/Python-${VERSION}.tar.xz
START=$(date)
tar xf Python-${VERSION}.tar.xz
cd Python-${VERSION}
./configure
make -j 4
sudo make altinstall
cd ..
#sudo rm -r Python-${VERSION}
#rm Python-${VERSION}.tar.xz

echo "Started at: ${START}"
echo "Ended at  : $(date)"

