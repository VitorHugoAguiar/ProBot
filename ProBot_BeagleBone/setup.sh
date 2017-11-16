#!/usr/bin/env bash

CheckInternet(){
case "$(curl -s --max-time 2 -I http://google.com | sed 's/^[^ ]*  *\([0-9]\).*/\1/; 1q')" in
  [23]) echo "";;
  5) echo "The web proxy won't let us through"
  exit 1;;
  *) echo "The network is down or very slow"
  exit 1;;
esac
}

ServerIPconfiguration() {
echo ""
read -p "--> Please enter the ProBot Server ip address: " broker
while true; do
    read -p "    Confirm (Y/N)? " yn
    case $yn in
        [Yy]* ) echo "    OK"; sed -i "/self.broker/c \       \ self.broker='${broker}'" ProBotConstantsFile.py; break;;
        [Nn]* ) exit;;
        * ) echo "Please answer yes or no.";;
    esac
done
}


ProBot_ID() {
echo ""
read -p "--> Please enter the ProBot ID: " probotID
while true; do
    read -p "    Confirm (Y/N)? " yn
    case $yn in
        [Yy]* ) echo "    OK"; sed -i "/self.probotID/c \       \ self.probotID='${probotID}'" ProBotConstantsFile.py; break;;
        [Nn]* ) exit;;
        * ) echo "Please answer yes or no.";;
    esac
done    

(crontab -l ; echo "@reboot sh $(pwd -P)/enableEQEP.sh") 2>&1 | grep -v "no crontab" | sort | uniq | crontab -
(crontab -l ; echo "@reboot sleep 20 && python $(pwd -P)/mqtt.py") 2>&1 | grep -v "no crontab" | sort | uniq | crontab -
(crontab -l ; echo "@reboot sleep 30 && python $(pwd -P)/ProBot.py 2") 2>&1 | grep -v "no crontab" | sort | uniq | crontab -
}


RealTimeKernel(){
echo ""
echo "--> Installing Real Time Kernel"
apt-get update -qq > /dev/null
apt-get upgrade -qq -y > /dev/null
apt-get install -qq -y linux-image-4.9.49-ti-xenomai-r58 > /dev/null
apt-get install -qq -y linux-headers-4.9.49-ti-xenomai-r58 > /dev/null
echo "    OK"
}


NetworkManager(){
echo ""
while true; do
    read -p "--> Do you want to install Network-Manager? (Y/N)? " yn
    case $yn in
        [Yy]* ) apt-get install -qq -y network-manager firmware-ralink > /dev/null; echo "    OK"; break;;
        [Nn]* ) break;;
        * ) echo "Please answer yes or no.";;
    esac
done
}

OtherStuff(){
echo ""
echo "--> Installing dependencies"
apt-get install -qq -y build-essential python-dev python-pip python-smbus python-serial python-memcache > /dev/null
pip install paho-mqtt==1.2.3 > /dev/null
git clone -q git://github.com/adafruit/adafruit-beaglebone-io-python.git 
cd adafruit-beaglebone-io-python
python setup.py install > /dev/null 2>&1
cd ..
rm -rf adafruit-beaglebone-io-python
echo "    OK";
}

main() {
CheckInternet
ServerIPconfiguration
ProBot_ID
NetworkManager
RealTimeKernel
OtherStuff
echo "Please reboot the BeagleBone..."
}
main "$@"
