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
    bash install_bootScripts.sh
fi

if echo "$answer" | grep -iq "^y" ;then
    echo "OK!"
else
    echo "Learn to write please X)"
    bash install_bootScripts.sh
fi

(sudo crontab -l ; echo "@reboot sleep 20 && python $(pwd -P)/WebClient.py $input_variable:$input_variable2") 2>&1 | grep -v "no crontab" | sort | uniq | crontab -
(sudo crontab -l ; echo "@reboot sh $(pwd -P)/EnableEncoders.sh") 2>&1 | grep -v "no crontab" | sort | uniq | crontab -
(sudo crontab -l ; echo "@reboot python $(pwd -P)/forward_ZMQ_Client.py") 2>&1 | grep -v "no crontab" | sort | uniq | crontab -
(sudo crontab -l ; echo "@reboot python $(pwd -P)/RestartProgram_ZMQ.py") 2>&1 | grep -v "no crontab" | sort | uniq | crontab -
(sudo crontab -l ; echo "@reboot python $(pwd -P)/RestartProgram.py") 2>&1 | grep -v "no crontab" | sort | uniq | crontab -
