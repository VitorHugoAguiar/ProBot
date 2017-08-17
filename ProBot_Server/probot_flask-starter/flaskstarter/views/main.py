# imports
from flask import Blueprint, render_template, request, jsonify, session, flash
from .. import app
from ..models import Probot
from datetime import timedelta
from apscheduler.scheduler import Scheduler
from ..forms.forms import ContactForm
from flask.ext.mail import Message, Mail
from ..email import send_email
import flask.ext.login
import paho.mqtt.client as mqtt
import paho.mqtt.publish as publish
import json
import time
import atexit
import os

main = Blueprint('main', __name__)

# variables
numberProbots = 6
busyProbots=[0]*(numberProbots+1)
OnlineProbots=[0]*(numberProbots+1)
StartUsingProbot=[0]*(numberProbots+1)
incomingMsg=0
broker = '89.109.64.175'
port = 1883
client = 0
cron = Scheduler(daemon=True)

# paho-mqtt
def on_connect(client, userdata, rc):
    print("Connected with result code " + str(rc))
    client.subscribe('telemetry', qos=0)
    client.subscribe('ClientStatus', qos=0)

def on_message(client, userdata, msg):
    global incomingMsg
    global OnlineProbots

    if msg.topic=="telemetry":
    	incomingMsg=msg.payload.split(",")
    	OnlineProbots[int(incomingMsg[0])]=incomingMsg

    if msg.topic=="ClientStatus":
    	incomingMsg=msg.payload.split("/")
    	OnlineProbots[int(incomingMsg[0])]=incomingMsg
    			
def on_disconnect(client, userdata, rc):
    global OnlineProbots
    	
    print("Disconnected with result code " + str(rc))
    for i in range (1, numberProbots+1):     
    	OnlineProbots[i]=[str(i), 'OFF-LINE']

# initialize cron and paho-mqtt only one time
@app.before_first_request
def initialize():
    global client
    cron.start()
    client = mqtt.Client(protocol=mqtt.MQTTv311)    
    client.connect(broker, port)
    client.on_connect = on_connect
    client.on_message = on_message
    client.on_disconnect = on_disconnect
    client.loop_start()    

# check which probot is being use
@cron.interval_schedule(seconds=0.5)
def job_function():
	for i in range (1,len(StartUsingProbot)):
		checkUsingProbot=time.time()
		delta=checkUsingProbot-StartUsingProbot[i]		
		if delta>=3:
			busyProbots[i]='0'
		
# render the web pages
@app.route('/', methods=['GET', 'POST'])
def index():
	"""Index."""
	return render_template('index.html')
	
@app.route('/probots_admin', methods=['GET', 'POST'])
def probots_admin():
	return render_template('probots_admin.html')
	
@app.route('/probot1_visit_UMa', methods=['GET', 'POST'])
def probot1_visit_UMa():
	"""probot1_visit_UMa"""
	return render_template('probot1_visit_UMa.html')

@app.route('/probot1_vs_probot2', methods=['GET', 'POST'])
def probot1_vs_probot2():
	"""probot1_vs_probot2"""
	return render_template('probot1_vs_probot2.html')

@app.route('/probot3_construction', methods=['GET', 'POST'])
def probot3_construction():
	"""probot3_construction"""
	return render_template('probot3_construction.html')

@app.route('/probot3_tests', methods=['GET', 'POST'])
def probot3_tests():
	"""probot3_tests"""
	return render_template('probot3_tests.html')

@app.route('/probot3_carnival', methods=['GET', 'POST'])
def probot3_carnival():
	"""probot3_carnival"""
	return render_template('probot3_carnival.html')	
	
@app.route('/probots_user', methods=['GET', 'POST'])
def probots_user():
		global busyProbots
		global StartUsingProbot		
		if request.method == 'POST':			# ALL went good		
			chosen_probot_id = request.form['options']	# Get chosen probot id from the form
			if request.user_agent.platform == ('android' or 'iphone' or 'ipad'): # check which platform we are
				if busyProbots[int(chosen_probot_id)]=='0': # checks if the chosen probot is available
					busyProbots[int(chosen_probot_id)]=str(chosen_probot_id)
					StartUsingProbot[int(chosen_probot_id)]=time.time()					
					return render_template('probot_control_mobile.html', chosen_probot_id=chosen_probot_id)
				else:
					return render_template('probots_user.html', not_available=1)
				
			else:				
					if busyProbots[int(chosen_probot_id)]=='0':
						busyProbots[int(chosen_probot_id)]=str(chosen_probot_id)
						StartUsingProbot[int(chosen_probot_id)]=time.time()					
						return render_template('probot_control_desk.html', chosen_probot_id=chosen_probot_id) 
					else:
						return render_template('probots_user.html', not_available=1)
						
		return render_template('probots_user.html', not_available=0)

# get info from the web page, which probot is in use and when is available again    
@app.route('/WebpageToServer', methods=['GET', 'POST'])
def WebpageToServer():
    chosen_probot_id = list(json.dumps(request.form['chosen_probot_id']))
    chosen_probot_id = [e for e in chosen_probot_id if e not in (',', '"', '"')]

    for i in range (len(chosen_probot_id)): 	   	
    	if (chosen_probot_id[i]==str(i+1)):
    		busyProbots[int(i+1)]=str(i+1)
    		StartUsingProbot[int(i+1)]=time.time()
    	if (chosen_probot_id[i]=='0'):
    		busyProbots[int(i+1)]='0'    		    		
    return b"0"

# publish the keys controls values to the right topic (probot)
@app.route('/WebpageKeys', methods=['GET', 'POST'])
def WebpageKeys():
    probot_ID = str (json.loads(request.form['probot_ID']))
    keyUp = str(json.loads(request.form['keyUp']))
    keyDown = str (json.loads(request.form['keyDown']))
    keyLeft = str (json.loads(request.form['keyLeft']))
    keyRight = str (json.loads(request.form['keyRight']))    
    
    keys = keyUp + " " + keyDown + " " + keyLeft + " " + keyRight          
    topic = 'keys/' + probot_ID
    client.publish(topic, keys, qos=0)
         		    		
    return b"0"
    
# publish the MainRoutine value to the right topic (probot)
@app.route('/MainRoutine', methods=['GET', 'POST'])
def MainRoutine():
    probot_ID = str (json.loads(request.form['probot_ID']))
    MainRoutineStatus = json.dumps(request.form['MainRoutineStatus'])
             
    topic = 'MainRoutine/' + probot_ID
    client.publish(topic, MainRoutineStatus, qos=0)
         		    		
    return b"0"    


# publish the shutdownProBot value to the right topic (probot)
@app.route('/shutdownProBot', methods=['GET', 'POST'])
def shutdownProBot():
    probot_ID = str (json.loads(request.form['probot_ID']))
    shutdownProBotStatus = json.dumps(request.form['shutdownProBotStatus'])
         
    topic = 'shutdownProBot/' + probot_ID
    client.publish(topic, shutdownProBotStatus, qos=0)
         		    		
    return b"0" 

# send tho the web page which probots is available    
@app.route('/ServerToWebpage', methods=['GET'])
def ServerToWebpage():
    return jsonify(busyProbots=busyProbots, OnlineProbots=OnlineProbots)

@app.route('/contact', methods=['GET', 'POST'])
def contact():
  form = ContactForm(request.form)
 
  if request.method == 'POST':
    if form.validate() == False:
      flash('All fields are required.')
      return render_template('contact.html', form=form)
    else:
      html = render_template(
            'user/contact_us.html',
            name=form.name.data,
            email=form.email.data,
            subject=form.subject.data,
            message=form.message.data
      )
      subject = 'Contact from robotcommander'
      send_email(os.environ['CONTACT_EMAIL'], subject, html)
      return render_template('contact.html', success=True)

  elif request.method == 'GET':
    return render_template('contact.html', form=form)

