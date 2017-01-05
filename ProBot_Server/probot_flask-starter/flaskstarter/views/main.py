from flask import Blueprint, render_template, request, flash, redirect, url_for
from .. import app, db
from ..models import Probot
from flask.ext.login import login_required
import json
from flask import jsonify
main = Blueprint('main', __name__)

available_probot = {}
@app.route('/', methods=['GET', 'POST'])
def index():
	"""Index."""
	return render_template('index.html')
	
@app.route('/probots', methods=['GET', 'POST'])
@login_required
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

@app.route('/bridge', methods=['POST'])
def message():
    probot_id = None
    battery = None
    body = json.loads(request.get_data())
    probot_id = int(body["args"][0])
    probot = Probot.query.filter_by(id = probot_id).first()
    
    if body["args"][2] == "UPDATE":
        probot.battery = int((body["args"][1]))
        
        if probot.is_available == 2:
            probot.is_available = 0   
        elif probot.is_available == 3:
            probot.is_available = 1
            
    elif body["args"][2] == "BATTERY TIMEOUT":
        if probot.is_available == 0:
            probot.is_available = 2
        elif probot.is_available == 1:
            probot.is_available = 3

    elif body["args"][2] == "WEB TIMEOUT":
        if probot.is_available == 0:
            probot.is_available = 1
    
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
    return jsonify(available_probot=available_probot)



