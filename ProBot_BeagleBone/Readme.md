How to configure the ProBot BeagleBone:

1 - Install the lastest debian image [from here]
(https://beagleboard.org/latest-images). 

2 - Install machinekit following the instructions [from here] (https://github.com/machinekit/machinekit-docs/blob/master/machinekit-documentation/getting-started/installing-packages.asciidoc).

3 - The HDMI port causes interference on the functioning of the USB port and some Encoders GPIO's. To disable it, remove the # in front of the cape_disable command on the /boot/uEnv.txt so it looks like: 

    ##Disable HDMI
    cape_disable=capemgr.disable_partno=BB-BONELT-HDMI,BB-BONELT-HDMIN

4 - To Install network-manager 1.0.4, run:

	sudo sh install_NetworkManager-1.0.4.sh
	
5 - Install the encoders running the following command:

	sudo sh install_Encoders.sh
	
6 - Install crossbar running:

	sudo sh install_Crossbar.sh
	
7 - Install zmq and smbus with:
    
    sudo apt-get -y install python-zmq python-smbus

8 - To enable on the boot the execution of some scripts required, type:

	sudo sh install_bootScripts.sh 
	
Note: Don't forget to change the path to this files and the server's ip

9 - Restart BeagleBone	

10 - Run:

	cd ProBot/ProBot_BeagleBone
	sudo python ProBot.py
