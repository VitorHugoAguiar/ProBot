How to configure the ProBot BeagleBone:

1 - Install the lastest debian image [from here]
(https://beagleboard.org/latest-images). 

2 - Make the update with:

	sudo apt-get update
	
3 - Install machinekit following the instructions [from here] (https://github.com/machinekit/machinekit-docs/blob/master/machinekit-documentation/getting-started/installing-packages.asciidoc).

4 - The HDMI port causes interference on the functioning of the USB port and some Encoders GPIO's. To disable it, remove the # in front of the cape_disable command on the /boot/uEnv.txt so it looks like: 

    ##Disable HDMI
    cape_disable=capemgr.disable_partno=BB-BONELT-HDMI,BB-BONELT-HDMIN

5 - Use git clone to download the ProBot's files.
	
	git clone https://github.com/VitorHugoAguiar/ProBot.git

6  - Go to ProBot_BeagleBone with::
	
	cd ProBot/ProBot_BeagleBone
and:

6.1 - To Install network-manager 1.0.4, run:

	sudo sh install_NetworkManager-1.0.4.sh
	
6.2 -  Install the encoders running the following command:

	sudo sh install_Encoders.sh
	
6.3 -  Install crossbar running:

	sudo sh install_Crossbar.sh

6.4 - To enable on the boot the execution of some scripts required, type:

	sudo sh install_bootScripts.sh 
	
Note: Open the install_bootScripts.sh and change the files path and the server's ip.

7 - Restart BeagleBone	

8 - Go again to ProBot/ProBot_BeagleBone and run ProBot.py to iniatiliaze the program:

	cd ProBot/ProBot_BeagleBone
	sudo python ProBot.py
