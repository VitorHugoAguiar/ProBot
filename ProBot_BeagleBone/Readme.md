How to configure the ProBot BeagleBone:

1 - Install the lastest debian image [from here]
(https://beagleboard.org/latest-images). 


2 - Install machinekit following the instructions [from here] (https://github.com/machinekit/machinekit-docs/blob/master/machinekit-documentation/getting-started/installing-packages.asciidoc).

3 - The HDMI port causes interference on the functioning of the USB port and some Encoders GPIO's. To disable it, remove the # in front of the cape_disable command on the /boot/uEnv.txt so it looks like: 

    ##Disable HDMI
    cape_disable=capemgr.disable_partno=BB-BONELT-HDMI,BB-BONELT-HDMIN

4 - Use git clone to download the ProBot's files.
	
	git clone https://github.com/VitorHugoAguiar/ProBot.git

5 - To Install network-manager 1.0.4, run:

	sudo sh install_NetworkManager-1.0.4.sh
	
6 -  Install the encoders running the following command:

	sudo sh install_Encoders.sh
	
7 -  Install crossbar running:

	sudo sh install_Crossbar.sh

8 - To enable on the boot the execution of some scripts required, type:

	sudo sh install_bootScripts.sh 
	
Note: Open the install_bootScripts.sh and change the files path and the server's ip.

9 - Restart BeagleBone	

10 - Run:

	sudo python ProBot.py
