#!/bin/sh

echo "Please enter the ProBot Server ip: "
read input_variable
echo "Please enter the port that you gonna use: "
read input_variable2
echo "Your ip is: $input_variable"
echo "Your port is: $input_variable2"

echo -n "Confirm (Y/N): "
read answer

if echo "$answer" | grep -iq "^n" ;then
    echo "Try again please!!!"
    bash install_everythingProBot.sh
fi

if echo "$answer" | grep -iq "^y" ;then
    echo "OK!"
else
    echo "Learn to write please X)"
    bash install_everythingProBot.sh
fi

export LANGUAGE=en_US.UTF-8
export LC_ALL=en_US.UTF-8
export LANG=en_US.UTF-8
export LC_TYPE=en_US.UTF-8

(sudo crontab -l ; echo "@reboot sleep 20 && python $(pwd -P)/WebClient.py $input_variable:$input_variable2") 2>&1 | grep -v "no crontab" | sort | uniq | crontab -
(sudo crontab -l ; echo "@reboot sh $(pwd -P)/EnableEncoders.sh") 2>&1 | grep -v "no crontab" | sort | uniq | crontab -
(sudo crontab -l ; echo "@reboot python $(pwd -P)/forward_ZMQ_Client.py") 2>&1 | grep -v "no crontab" | sort | uniq | crontab -
(sudo crontab -l ; echo "@reboot python $(pwd -P)/RestartProgram_ZMQ.py") 2>&1 | grep -v "no crontab" | sort | uniq | crontab -
(sudo crontab -l ; echo "@reboot python $(pwd -P)/RestartProgram.py") 2>&1 | grep -v "no crontab" | sort | uniq | crontab -

sudo sh -c \
"echo 'Package: *
Pin: release a=stable
Pin-Priority: 900

Package: *
Pin: release o=Debian
Pin-Priority: -10' > \
/etc/apt/preferences.d/sid;"

sudo echo 'deb http://ftp.nl.debian.org/debian/ jessie main' >> /etc/apt/sources.list
sudo echo 'deb-src http://ftp.nl.debian.org/debian/ jessie main' >> /etc/apt/sources.list
sudo echo 'deb http://ftp.nl.debian.org/debian/ sid main' >> /etc/apt/sources.list
sudo echo 'deb-src http://ftp.nl.debian.org/debian/ sid main' >> /etc/apt/sources.list

sudo apt-get update

sudo apt-get install -y -t sid libczmq-dev

sudo rm -rf /etc/apt/apt.conf.d/02compress-indexes 
sudo apt-get update
sudo apt-get install -y xauth
sudo apt-get install -y apt-show-versions

sudo apt-key adv --keyserver keyserver.ubuntu.com --recv 43DDF224
sudo sh -c \
  "echo 'deb http://deb.machinekit.io/debian jessie main' > \
  /etc/apt/sources.list.d/machinekit.list"
  
sudo apt-get update

sudo apt-get install -y linux-image-3.8.13-xenomai-r78 
sudo apt-get install -y machinekit-xenomai machinekit-dev

echo "MACHINEKIT INSTALLED!!!"

sudo apt-get -y install intltool libdbus-glib-1-dev libgudev-1.0-dev libnl-3-dev libnl-route-3-dev libnl-genl-3-dev uuid-dev libreadline-dev libnss3-dev ppp-dev libndp-dev python-gi python-dbus libnewt-dev python-zmq python-smbus build-essential libssl-dev libffi-dev python-dev
sudo python get-pip.py
sudo pip install --upgrade six
sudo pip install --upgrade setuptools

tar xf NetworkManager-1.0.4.tar.xz
cd NetworkManager-1.0.4

sudo ./configure --prefix=/usr\
    --sysconfdir=/etc    \
    --localstatedir=/var \
    --with-nmtui         \
    --disable-ppp        \
    --with-systemdsystemunitdir=no \
    --docdir=/usr/share/doc/network-manager-1.0.4

sudo make && sudo make install

sudo cp network-manager /etc/init.d && sudo cp NetworkManager.conf /etc/NetworkManager && sudo update-rc.d network-manager defaults

echo "NETWORK MANAGER INSTALLED!!!"

cd ..
cd encoders
sudo cp bone_eqep0-00A0.dtbo /lib/firmware
sudo cp bone_eqep1-00A0.dtbo /lib/firmware
sudo cp bone_eqep2-00A0.dtbo /lib/firmware
sudo cp bone_eqep2b-00A0.dtbo /lib/firmware

echo "ENCODERS INSTALLED!!!"

sudo pip install crossbar

echo "CROSSBAR INSTALLED!!"
echo "Now restart the BeagleBone and you are ready to go!!!!"
