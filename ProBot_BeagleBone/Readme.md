How to configure the ProBot BeagleBone:

1 - Install debian image

2 - Run 
	
	apt-get update

3 - Disable HDMI on the /boot/uEnv.txt

4 - Install network-manager 1.0.4 (follow the instructions that are within the folder NetworkManager-1.0.4)

5 - Install Xenomai and make the latency test

    http://syrianspock.github.io/embedded-linux/2015/08/03/xenomai-installation-on-a-beaglebone-black.html

6 - Install zmq and smbus with:
    
    apt-get install python-zmq python-smbus

7 - Install the encoders running the following command: 

	cd ProBot/ProBot_BeagleBone/ProBot_BeagleBone_Configuration/encoders
	cp bone_eqep0-00A0.dtbo /lib/firmware

8 - Use the same command for the others encoders files

9 - Install crossbar (follow the instructions that are within the folder Crossbar)

11 - Type "crontab -e" and write:

	@reboot sh /root/ProBot/ProBot_BeagleBone/EnableEncoders.sh
	
	@reboot python /root/ProBot/ProBot_BeagleBone/forward_device1.py
	
	@reboot sleep 20 && python /root/ProBot/ProBot_BeagleBone/WebClient.py ws://(ip of the server)
	
12 - Run:
	cd ProBot/ProBot_BeagleBone
	python ProBot.py
