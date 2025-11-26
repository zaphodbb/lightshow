# Prepare OS
# Set up ~/.ssh, github key, and config file
sudo apt-get install git python3-dev build-essential
sudo mkdir /opt/lightshow
sudo chown sean:sean /opt/lightshow
cd /opt
git clone git@github.com:zaphodbb/lightshow.git
cd lightshow
python -m venv venv
source venv/bin/activate
python -m pip install Adafruit-Blinka adafruit-circuitpython-led-animation adafruit-circuitpython-neopixel adafruit-circuitpython-pixelbuf socketio RPi.GPIO rpi-ws281x

