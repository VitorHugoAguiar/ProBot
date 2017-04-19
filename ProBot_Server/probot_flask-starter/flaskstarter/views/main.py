from flask import Blueprint, render_template, request, flash, redirect, url_for
from .. import app, db
from ..models import Probot
from flask.ext.login import login_required
import json
from flask import jsonify
main = Blueprint('main', __name__)

available_probot = {}
available_probot2 = {}
availableWeb_probot = {}
availableWeb_probot2 = []

@app.route('/', methods=['GET', 'POST'])
def index():
	"""Index."""
	return render_template('index.html')

@app.route('/gallery', methods=['GET', 'POST'])
def gallery():
	"""gallery."""
	return render_template('gallery.html')
	
@app.route('/probots', methods=['GET', 'POST'])
def probots():

	global available_probot		#variable to control the HTML content, True: Shows the form 
	probots_available_db = Probot.query.filter((Probot.is_available == 1) & (Probot.battery >= 20)).all()

	if probots_available_db == []:	#NO probots available
		print("available_probot", available_probot)
		available_probot = {}

	else:							#At least one probot available

		available_probot=[(probot.id) 
			for probot in probots_available_db]
		
		print("available_probot", available_probot)

		if request.method == 'POST':			#ALL went good
		
			chosen_probot_id = request.form['options']	#Get chosen probot id from the form
			chosen_probot = Probot.query.filter_by(id = chosen_probot_id).first()			
			chosen_probot.is_available = 0
			
			try:
				db.session.add(chosen_probot)
				db.session.commit()               
			except:			
				db.session.rollback()
				error_msg = 'Could not change the ProBot\'s availability'
				flash(error_msg, 'warning')
				raise
			finally:
				db.session.close()
			
			if request.user_agent.platform == ('android' or 'iphone' or 'ipad'):

				return render_template('botcontrolphone.html', chosen_probot_id=chosen_probot_id)				
			else:
				return render_template('botcontrol.html', chosen_probot_id=chosen_probot_id) #render the file with the probot control "console"

	return render_template('probots.html', field=available_probot)
	
@app.route('/probots_admin', methods=['GET', 'POST'])
@login_required
def probots_admin():

	global available_probot2		#variable to control the HTML content, True: Shows the form 
	probots_available_db = Probot.query.filter((Probot.is_available == 1) or (Probot.is_available == 2)).all()

	if probots_available_db == []:	#NO probots available
		available_probot = {}

	else:							#At least one probot available

		available_probot2=[(probot.id) 
			for probot in probots_available_db]

	return render_template('probots_admin.html', field=available_probot2)



@app.route('/bridge', methods=['POST'])
def message():
    global availableWeb_probot
    global availableWeb_probot2
    probot_id = None
    battery = None
    body = json.loads(request.get_data())
    probot_id = int(body["args"][0])
    probot = Probot.query.filter_by(id = probot_id).first()
    availableWeb_probot3=[]
    #ProBots status -> 0 - Not avaiable
    #				   1 - Avaiable
    #				   2 - Waiting for the baterry value			
    if body["args"][2] == "UPDATE":
        probot.battery = int((body["args"][1]))
        if probot.is_available == 2:
            probot.is_available = 1
            
    elif body["args"][2] == "BATTERY TIMEOUT":
		probot.is_available = 2
		
    elif body["args"][2] == "WEB TIMEOUT":
        if probot.is_available == 0:
            probot.is_available = 2
            
    availableWeb_probot[probot_id]=probot.is_available
    for index, elem in enumerate(availableWeb_probot):
        availableWeb_probot3.insert(index, availableWeb_probot[elem])
    availableWeb_probot2=availableWeb_probot3
    
    try:
        db.session.add(probot)
        db.session.commit()
        probot_id = None               
    except:			
        db.session.rollback()
        probot_id = None
        raise
    finally:
        db.session.close()
 
    return b"OK"
    
    
@app.route('/checkProbotOnline', methods= ['GET'])
def checkProbotOnline():
    return jsonify(available_probot=available_probot, availableWeb_probot=availableWeb_probot2)
