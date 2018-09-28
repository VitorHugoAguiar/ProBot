# Probot BeagleBone

How to configure the ProBot BeagleBone:

Step 1 - Install the lastest debian image [from here](https://beagleboard.org/latest-images). 

Note: The Probot Project is working on a BeagleBone Black with debian 9.2 (jessie) and kernel 4.9.49-ti-xenomai-r58. 

Step 2 - The HDMI port causes interference on the functioning of the USB port and some Encoders GPIO's. To disable it, comment the following line on the /boot/uEnv.txt:

	disable_uboot_overlay_video=1

and change
    
	cape_disable=bone_capemgr.disable_partno=
to

	cape_disable=bone_capemgr.disable_partno=BB-BONELT-HDMI,BB-BONELT-HDMIN

Step 2.1 - In order to get the Encoders working, we have to enable the universal cape. For that, on the /boot/uEnv.txt, change the following lines:

	cmdline=coherent_pool=1M net.ifnames=0 quiet

to 

	cmdline=coherent_pool=1M net.ifnames=0 quiet cape_universal=enable

and

	cape_enable=bone_capemgr.enable_partno=
to

	cape_enable=bone_capemgr.enable_partno=cape_universala
	

Step 3 - Use git clone to download all files:
	
	git clone https://github.com/VitorHugoAguiar/ProBot.git

or install subversion
	
	sudo apt-get install subversion

and do
	
	svn export https://github.com/VitorHugoAguiar/ProBot.git/trunk/ProBot_BeagleBone

to download only the BeagleBone files. 

	
Step 4  - To install everything that it's required to run ProBot's program, for debian images (jessie), just type:
	
	sudo ./setup.sh


Step 5 - To configure the networks and the BeagleBone's ip with network-manager, type:

	sudo nmtui	
	

Step 6 - Go again to ProBot/ProBot_BeagleBone and run ProBot.py to initialize the program:

	sudo python ProBot.py

