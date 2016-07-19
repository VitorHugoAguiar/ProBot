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

(sudo crontab -l ; echo "@reboot sleep 20 && python $(pwd -P)/WebClient.py ws://$input_variable:$input_variable2") 2>&1 | grep -v "no crontab" | sort | uniq | crontab -
(sudo crontab -l ; echo "@reboot sh $(pwd -P)/EnableEncoders.sh") 2>&1 | grep -v "no crontab" | sort | uniq | crontab -
(sudo crontab -l ; echo "@reboot python $(pwd -P)/forward_ZMQ_Client.py") 2>&1 | grep -v "no crontab" | sort | uniq | crontab -

cd ..
cd Machinekit
sudo sh install_Machinekit.sh

cd ..
cd Encoders
sudo sh install_Encoders.sh

cd ..
cd Crossbar
sudo sh install_Crossbar.sh

cd ..
cd SaltMinion
sudo sh install_SaltMinion.sh

sudo shutdown -h now
