How to configure the ProBot BeagleBone:

1 - Install debian image

2 - Run 
	
	apt-get update

3 - Disable HDMI on the /boot/uEnv.txt

4 - Install network-manager 1.0.4 (follow the instructions that are within the folder NetworkManager-1.0.4)

5 - Run Xenomai and make the latency test

6 - Install zmq and smbus with:
    
    apt-get install python-zmq python-smbus

7 - Install the encoders from beaglebot running the following command: 

	cp encoders/bone_eqep0-00A0.dtbo /lib/firmware

8 - Use the same command for the others encoders files

9 - Install crossbar (follow the instructions that are within the folder Crossbar)

10 - Copy the folder "ProBot_BeagleBone" to the BeagleBone

11 - Type "crontab -e" and write:

	@reboot sh /root/ProBot_BeagleBone/EnableEncoders.sh
	
	@reboot python /root/ProBot_BeagleBone/forward_device1.py
	
	@reboot sleep 20 && python /root/ProBot_BeagleBone/WebClient.py ws://(ip of the server)
	
12 - Run:
	
	python ProBot_BeagleBone/ProBot.py
