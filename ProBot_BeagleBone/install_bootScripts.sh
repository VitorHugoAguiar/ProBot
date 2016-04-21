#!/bin/sh
set -ex
(sudo crontab -l ; echo "@reboot sleep 20 && python $(pwd -P)/WebClient.py $input_variable:$input_variable2") 2>&1 | grep -v "no crontab" | sort | uniq | crontab -
(sudo crontab -l ; echo "@reboot sh $(pwd -P)/EnableEncoders.sh") 2>&1 | grep -v "no crontab" | sort | uniq | crontab -
(sudo crontab -l ; echo "@reboot python $(pwd -P)/forward_ZMQ_Client.py") 2>&1 | grep -v "no crontab" | sort | uniq | crontab -
(sudo crontab -l ; echo "@reboot python $(pwd -P)/RestartProgram_ZMQ.py") 2>&1 | grep -v "no crontab" | sort | uniq | crontab -
(sudo crontab -l ; echo "@reboot python $(pwd -P)/RestartProgram.py") 2>&1 | grep -v "no crontab" | sort | uniq | crontab -
