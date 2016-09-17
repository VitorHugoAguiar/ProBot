# Probot BeagleBone

How to configure the ProBot BeagleBone:

1 - Install the lastest debian image [from here]
(https://beagleboard.org/latest-images). 

Note: The Probot Project is working on a BeagleBone Black with debian 8.2 (jessie). 

2 - The HDMI port causes interference on the functioning of the USB port and some Encoders GPIO's. To disable it, remove the # in front of the cape_disable command on the /boot/uEnv.txt so it looks like: 

    ##Disable HDMI
    cape_disable=capemgr.disable_partno=BB-BONELT-HDMI,BB-BONELT-HDMIN

3 - Use git clone to download the ProBot's files.
	
	git clone https://github.com/VitorHugoAguiar/ProBot.git

4  - Go to ProBot_BeagleBone with::
	
	cd ProBot/ProBot_BeagleBone/InstallEverything
and:

4.1 - To install everything that it's required to run ProBot's program, for debian images (jessie), just type:

	sudo sh install_everythingProBot.sh

This file is gonna install:

	Machinekit
	Network-Manager
	Encoders
	Crossbar

Note: After the installation the BeagleBone is gonna shutdown.

5 - To configure the networks and the BeagleBone's ip, type.

	sudo nmtui	

6 - Go again to ProBot/ProBot_BeagleBone and run ProBot.py to initialize the program:

	cd ProBot/ProBot_BeagleBone
	sudo python ProBot.py
	
If you just want to install some files or libraries, follow the next instructions:

7 - Go to:

	cd ProBot/ProBot_BeagleBone

and:

7.1 - To install just machinekit, for debian images (jessie), type:
	
	sudo sh install_machinekit.sh

7.2 - To Install network-manager, run:

	sudo apt-get -y install network-manager

Note: After network manager been installed, type:
	
	sudo nmtui
	
and configure the networks and the BeagleBone's ip.

7.3 -  Install the encoders running the following command:

	sudo sh install_Encoders.sh
	
7.4 -  Install crossbar running:

	sudo pip install crossbar
