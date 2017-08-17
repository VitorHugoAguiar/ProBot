# ProBot Server

# Flask
To control the Probots we are using a web page built with [Flask](http://flask.pocoo.org/). This code is based on [Flask-Starter](https://github.com/samgclarke/flask-starter).

With this interface, both admin and user can see the ProBots that are available to control. After choosing one ProBot, the user can see all the information related to that ProBot, like the angle or the battery percentage.

The admin can initialize the mainRoutine and shutdown the BeagleBone.

# Paho-mqtt and mosquitto
The communication between the ProBots (beaglebone) and the server, are made through the [paho-mqtt.](http://www.eclipse.org/paho/) To install paho-mqtt on the server, you need to type:
	
	sudo pip install paho-mqtt

The mqtt needs a message broker. For that, we are using [mosquitto.](https://mosquitto.org/) You can install mosquitto message broker by typing:
	
	sudo apt-get install mosquitto
	
After the mosquitto installation, is necessary to change the mosquitto.conf file with:
	
	sudo nano /etc/mosquitto/mosquitto.conf

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

You need to define the port for the ProBots (beaglebone) to communicate with the Server and for the websocket. In the end, the mosquitto.conf should look like:

	# Place your local configuration in /etc/mosquitto/conf.d/
	#
	# A full description of the configuration file is at
	# /usr/share/doc/mosquitto/examples/mosquitto.conf.example
	
	# ProBot/server communication port
	listener 1883

	pid_file /var/run/mosquitto.pid

	persistence true
	persistence_location /var/lib/mosquitto/

	log_dest topic

	log_type error
	log_type warning
	log_type notice
	log_type information

	connection_messages true
	log_timestamp true

	include_dir /etc/mosquitto/conf.d

	# WebSockets ports configuration
	listener 9001
	protocol websockets

	listener 9883
	protocol websockets
