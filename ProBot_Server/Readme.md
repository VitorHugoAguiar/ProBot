# ProBot Server

# Flask
To control the Probots  we are using web page build with [Flask](http://flask.pocoo.org/). This code is based on [Flask-Starter](https://github.com/samgclarke/flask-starter).

With this interface, the user can see the ProBots that are avaiable. After choose one ProBot, the user can see some useful information related to that ProBot like the angle or the battery percentage.

The admin can also initialize the mainRoutine and shutdown the BeagleBone.

# Paho-mqtt and mosquitto
For the communication between the ProBots (beaglebone) and the server, we are using the [paho-mqtt.](http://www.eclipse.org/paho/) To install paho-mqtt on the server, you need to type:
	
	pip install paho-mqtt

The mqtt needs a message broker. For that, we are using [mosquitto.](https://mosquitto.org/) You can install mosquitto message broker by typing:
	
	apt-get install mosquitto
	
After the mosquitto instalion, is necessary to change the mosquitto.conf file. For that, type:
	
	nano /etc/mosquitto/mosquitto.conf

The mosquitto.conf file should look like this:
	
	# Place your local configuration in /etc/mosquitto/conf.d/
	#
	# A full description of the configuration file is at
	# /usr/share/doc/mosquitto/examples/mosquitto.conf.example

	pid_file /var/run/mosquitto.pid

	persistence true
	persistence_location /var/lib/mosquitto/

	log_dest file /var/log/mosquitto/mosquitto.log

	include_dir /etc/mosquitto/conf.d

You need to include the port used by the ProBots(beaglebone) to communicate with the Server and the port used by the websocket. In the end, the mosquitto.conf should look like:

	# Place your local configuration in /etc/mosquitto/conf.d/
	#
	# A full description of the configuration file is at
	# /usr/share/doc/mosquitto/examples/mosquitto.conf.example
	
	# port used between probot and server
	listener 1883 

	pid_file /var/run/mosquitto.pid

	persistence true
	persistence_location /var/lib/mosquitto/

	log_dest file /var/log/mosquitto/mosquitto.log

	include_dir /etc/mosquitto/conf.d	
	
	# WebSockets
	listener 9883
	protocol websockets


	
