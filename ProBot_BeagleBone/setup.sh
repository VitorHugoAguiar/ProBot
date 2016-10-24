#!/usr/bin/env bash
set -eo pipefail; [[ $TRACE ]] && set -x

Server-IPconfiguration() {
echo ""
read -p "--> Please enter the ProBot Server ip: " server_ip

while true; do
    read -p "    Confirm (Y/N)? " yn
    case $yn in
        [Yy]* ) echo "    OK"; sed -i "s/\bserver_ip=\b/&$server_ip/" WebClient.py; break;;
        [Nn]* ) exit;;
        * ) echo "Please answer yes or no.";;
    esac
done

(crontab -l ; echo "@reboot sleep 20 && python $(pwd -P)/WebClient.py") 2>&1 | grep -v "no crontab" | sort | uniq | crontab -
(crontab -l ; echo "@reboot sh $(pwd -P)/EnableEncoders.sh") 2>&1 | grep -v "no crontab" | sort | uniq | crontab -
(crontab -l ; echo "@reboot python $(pwd -P)/forward_ZMQ_Client.py") 2>&1 | grep -v "no crontab" | sort | uniq | crontab -

}
	

NetworkManager(){

echo "--> Installing Network-Manager"
apt-get update -qq > /dev/null
apt-get -qq -y install network-manager firmware-ralink
echo "    Done"

}	
	
Machinekit(){

echo "--> Installing Machinekit"
apt-get update -qq > /dev/null

sh -c \
"echo 'Package: *
Pin: release a=stable
Pin-Priority: 900

Package: *
Pin: release o=Debian
Pin-Priority: -10' > \
/etc/apt/preferences.d/sid;"

grep -q -F 'deb http://ftp.nl.debian.org/debian/ jessie main' /etc/apt/sources.list || echo 'deb http://ftp.nl.debian.org/debian/ jessie main' >> /etc/apt/sources.list
grep -q -F 'deb-src http://ftp.nl.debian.org/debian/ jessie main' /etc/apt/sources.list || echo 'deb-src http://ftp.nl.debian.org/debian/ jessie main' >> /etc/apt/sources.list
grep -q -F 'deb http://ftp.nl.debian.org/debian/ sid main' /etc/apt/sources.list || echo 'deb http://ftp.nl.debian.org/debian/ sid main' >> /etc/apt/sources.list
grep -q -F 'deb-src http://ftp.nl.debian.org/debian/ sid main' /etc/apt/sources.list || echo 'deb-src http://ftp.nl.debian.org/debian/ sid main' >> /etc/apt/sources.list

rm -rf /etc/apt/apt.conf.d/02compress-indexes

apt-get update -qq > /dev/null

apt-get install -qq -y -t sid libczmq-dev
apt-get install -qq -y apt-show-versions

apt-key adv --keyserver keyserver.ubuntu.com --recv 43DDF224
sh -c \
  "echo 'deb http://deb.machinekit.io/debian jessie main' > \
  /etc/apt/sources.list.d/machinekit.list"

apt-get update
apt-get install -qq -y  xauth linux-image-3.8.13-xenomai-r78 linux-headers-3.8.13-xenomai-r78 machinekit-xenomai machinekit-dev

echo "--> Done"	

}

Encoders(){

echo "--> Installing Encoders"
mv bone_eqep0-00A0.dtbo /lib/firmware
mv bone_eqep1-00A0.dtbo /lib/firmware
mv bone_eqep2-00A0.dtbo /lib/firmware
mv bone_eqep2b-00A0.dtbo /lib/firmware
echo "    Done"	

}	


Crossbar(){

echo "--> Installing Crossbar"
apt-get install -qq -y build-essential libssl-dev libffi-dev python-dev python-smbus
python get-pip.py
rm -rf get-pip.py
pip install --upgrade six
pip install --upgrade setuptools
pip install  crossbar
echo "    Done"

}

Salt-minion(){
	
echo "--> Installing Salt-Minion"
grep -q -F 'deb http://httpredir.debian.org/debian jessie-backports main' /etc/apt/sources.list || echo 'deb http://httpredir.debian.org/debian jessie-backports main' >> /etc/apt/sources.list
grep -q -F 'deb http://httpredir.debian.org/debian stretch main'  /etc/apt/sources.list || echo 'deb http://httpredir.debian.org/debian stretch main' >> /etc/apt/sources.list
touch /etc/apt/apt.conf.d/10apt
grep -q -F 'APT::Default-Release "jessie";' /etc/apt/apt.conf.d/10apt || echo 'APT::Default-Release "jessie";' >> /etc/apt/apt.conf.d/10apt
apt-get update
apt-get install -y python-zmq python-tornado/jessie-backports salt-common/stretch
apt-get install -y salt-minion/stretch
echo "    Done"

}


main() {
Server-IPconfiguration
NetworkManager
Machinekit
Encoders
Crossbar
Salt-minion
echo "Installation finished"
echo "Beaglebone is gonna shutdown"
shutdown -h now
}

main "$@"
