How to configure the ProBot BeagleBone:

1 - Install debian image

2 - Run 
	
	sudo apt-get update

3 - Disable HDMI on the /boot/uEnv.txt

4 - Install network-manager 1.0.4 (follow the instructions that are within the folder NetworkManager-1.0.4)

5 - Install Xenomai [from here] (http://syrianspock.github.io/embedded-linux/2015/08/03/xenomai-installation-on-a-beaglebone-black.html) and make the latency test

6 - Install zmq and smbus with:
    
    sudo apt-get -y install python-zmq python-smbus

7 - Install the encoders running the following command: 

	cd ProBot/ProBot_BeagleBone/encoders
	sudo cp bone_eqep0-00A0.dtbo /lib/firmware

8 - Use the same command for the others encoders files

9 - Install crossbar (follow the instructions that are within the folder Crossbar)

11 - Type "crontab -e" and write:

	@reboot sh /(path to)/ProBot/ProBot_BeagleBone/EnableEncoders.sh
	@reboot python /(path to)/ProBot/ProBot_BeagleBone/forward_ZMQ_Client.py
	@reboot sleep 20 && python /(path to)/ProBot/ProBot_BeagleBone/WebClient.py ws://(server ip's):9000

12 - Restart BeagleBone	

13 - Run:

	cd ProBot/ProBot_BeagleBone
	sudo python ProBot.py
