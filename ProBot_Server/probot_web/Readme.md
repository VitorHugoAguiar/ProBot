# flask-starter

A starter application template for Flask, with Authentication and User Account.

To run flask-starter locally, you need to:

Step 1: Define some enviromment variables:

	export APP_SETTINGS="config.DevelopmentConfig"
	export DATABASE_URL=$PWD
	export CONTACT_EMAIL=YOUR@GMAIL
	export LOGGING_URL=localhost:514
	export APP_MAIL_USERNAME=YOURGMAILUSERNAME
	export APP_MAIL_PASSWORD=YOURGMAILPASS

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
