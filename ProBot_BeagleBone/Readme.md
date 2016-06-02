How to configure the ProBot BeagleBone:

1 - Install the lastest debian image [from here]
(https://beagleboard.org/latest-images). 

2 - The HDMI port causes interference on the functioning of the USB port and some Encoders GPIO's. To disable it, remove the # in front of the cape_disable command on the /boot/uEnv.txt so it looks like: 

    ##Disable HDMI
    cape_disable=capemgr.disable_partno=BB-BONELT-HDMI,BB-BONELT-HDMIN

3 - Use git clone to download the ProBot's files.
	
	git clone https://github.com/VitorHugoAguiar/ProBot.git

4  - Go to ProBot_BeagleBone with::
	
	cd ProBot/ProBot_BeagleBone
and:

4.1 - To install everything that it's required to run ProBot's program, for debian images, just type:

	sudo sh install_everythingProBot.sh

This file is gonna install:

	Machinekit
	Network Manager
	Encoders
	Crossbar
	bootScripts

5 - Restart BeagleBone

6 - To configure the networks and the BeagleBone's ip, type.

	sudo nmtui	

7 - Go again to ProBot/ProBot_BeagleBone and run ProBot.py to initialize the program:

	cd ProBot/ProBot_BeagleBone
	sudo python ProBot.py
	
if you just want to install some files or libraries, follow the next instructions:

8 - Go to:

	cd ProBot/ProBot_BeagleBone

and:

8.1 - To install just machinekit for debian images type:
	
	sudo sh install_machinekit.sh

8.2 - To Install network-manager 1.0.4, run:

	sudo apt-get install network-manager

Note: After network-manager been installed, type:
	
	sudo nmtui
	
and configure the networks and the BeagleBone's ip.

8.3 -  Install the encoders running the following command:

	sudo sh install_Encoders.sh
	
8.4 -  Install crossbar running:

	sudo sh install_Crossbar.sh
