How to configure the ProBot BeagleBone:

1 - Install debian image

2 - Run 
	
	apt-get update

3 - Disable HDMI on the /boot/uEnv.txt

4 - Install network-manager 1.0.4 (follow the instructions that are within the folder NetworkManager-1.0.4)

5 - Configure WiFi with the command "nmtui" and put a static ip on the BeagleBone

6 - Reboot and check the internet connection ("ping 8.8.8.8") and the BeagleBone ip's

7 - Run Xenomai and make the latency test

8 - Install zmq and smbus with:
    
    apt-get install python-zmq python-smbus

9 - Install the encoders from beaglebot running the following command: 

	cp encoders/bone_eqep0-00A0.dtbo /lib/firmware

10 - Use the same command for the others encoders files

11 - Install crossbar (follow the instructions that are within the folder Crossbar)

12 - Copy the folder "ProBot_BeagleBone" to the BeagleBone

13 - Type "crontab -e" and write:

	@reboot sh /root/ProBot_BeagleBone/EnableEncoders.sh
	
	@reboot python /root/ProBot_BeagleBone/forward_device1.py
	
	@reboot sleep 20 && python /root/ProBot_BeagleBone/WebClient.py ws://(ip of the server)
	
14 - Change the ip in the ProBot_BeagleBone/SocketCommunication.py file to the BeagleBone ip's.

15 - Run:
	
	python ProBot_BeagleBone/ProBot.py
