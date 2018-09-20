# project/user/views.py

#################
#### imports ####
#################

import datetime
import os
import time
import requests
import ast
import json
import sys
from apscheduler.scheduler import Scheduler
from atexit import register
from glob import glob
from datetime import timedelta
from natsort import natsorted, ns
import logging
logging.getLogger('apscheduler').setLevel(logging.CRITICAL)

from werkzeug.contrib.cache import SimpleCache
from flask import render_template, Blueprint, url_for, redirect, flash, request, jsonify, Flask, session
from flask_login import login_user, logout_user, login_required, current_user

from project.models import User
from project.email import send_email
from project.token import generate_confirmation_token, confirm_token
from project.decorators import check_confirmed, required_roles
from project.table import Results

from project import db, bcrypt, app
from .forms import LoginForm, RegisterForm, ChangePasswordForm, ForgotForm, DatabaseForm

import paho.mqtt.client as mqtt
import paho.mqtt.publish as publish



################
#### config ####
################

user_blueprint = Blueprint('user', __name__,)
main_blueprint = Blueprint('main', __name__,)


##################
#### memcache ####
##################

clientPymemcache = SimpleCache(default_timeout=0)
clientPymemcache.set('ProBotInUseDictTimeOut', {})
clientPymemcache.set('ProBotTelemetryDictTimeOut', {})
clientPymemcache.set('ProBotInUseDictTimeOutLocal', {})
clientPymemcache.set('ProBotNotInUse', {})
clientPymemcache.set('AllProBotsTelemetryList', "[['ProBot1', 'Offline'], ['ProBot2', 'Offline'], ['ProBot3', 'NotWorking'], ['ProBot4', 'NotWorking'], ['ProBot5', 'NotWorking'], ['ProBot6', 'NotWorking']]")
clientPymemcache.set('ProBotChosen', "[['ProBot1', 'Available'], ['ProBot2', 'Available'], ['ProBot3', 'Available'], ['ProBot4', 'Available'], ['ProBot5', 'Available'], ['ProBot6', 'Available']]")


###################
#### Scheduler ####
###################

cron = Scheduler(daemon=True)

####################
#### Paho-MQTT ####
####################

client = ''

def on_connect(client, userdata, rc):
    print("Connected with result code " + str(rc))
    client.subscribe('telemetry', qos=0)
    client.subscribe('ClientStatus', qos=0)   
    
def on_message(client, userdata, msg):
    ProBotTelemetryDictTimeOut = clientPymemcache.get('ProBotTelemetryDictTimeOut')

    if msg.topic == "telemetry":
        ProBotTelemetry = [msg.payload.split(",")]
        ProBotTelemetryDictTimeOut[ProBotTelemetry[0][0]] = time.time()
        
    if msg.topic == "ClientStatus":
        ProBotTelemetry = [msg.payload.split("/")]
        ProBotTelemetryDictTimeOut[ProBotTelemetry[0][0]] = None

    AllProBotsTelemetryList = ast.literal_eval(str(clientPymemcache.get('AllProBotsTelemetryList')))
    newsub_dict = {sub[0]: sub for sub in ProBotTelemetry}
    AllProBotsTelemetryList = [newsub_dict.get(sub[0], sub) for sub in AllProBotsTelemetryList]


    clientPymemcache.set('AllProBotsTelemetryList', AllProBotsTelemetryList)
    clientPymemcache.set('ProBotTelemetryDictTimeOut', ProBotTelemetryDictTimeOut)    
    

def on_disconnect(client, userdata, rc):	
    print("Disconnected with result code " + str(rc))


################
#### routes ####
################


@user_blueprint.before_app_first_request
def __init__():
    global client
    session.permanent = True
    app.permanent_session_lifetime = timedelta(minutes=60)
    session.modified = True 
    client = mqtt.Client(protocol=mqtt.MQTTv311)  
    client.connect(app.config['MQTT_SERVER_IP'], app.config['MQTT_PORT'])
    client.on_connect = on_connect
    client.on_message = on_message
    client.on_disconnect = on_disconnect
    client.loop_start()
    cron.start() 
    register(lambda: cron.shutdown(wait=False)) 
    AlbunsPhotosPath()

def AlbunsPhotosPath ():
    listOfFiles = []
    directoryPath  = os.getcwd() + "/project/static/gallery/*" 
    albunsPath = glob(directoryPath)
    fileExtensions = [ "/*.jpg", "/*.JPG"]

    for i in range(0, len(albunsPath)):
        images = ""
        for extension in fileExtensions:
            photoPath = albunsPath[i] + extension
            for j in range(0 , len(glob(photoPath))):
                if j == len(glob(photoPath))-1:
                    images += glob(photoPath)[j].split("/")[-1]
                    ImagesOrdered = ','.join(map(str,natsorted(images.split(','), key=lambda y: y.lower()))) 
                else:
                    images += glob(photoPath)[j].split("/")[-1] + ","

                        
        listOfFiles.append([])

        listOfFiles[i].append(albunsPath[i].split("/")[-1])
        listOfFiles[i].append(ImagesOrdered)

    clientPymemcache.set('listOfFiles', listOfFiles)


def forms():
    loginForm = LoginForm(request.form)
    registerForm = RegisterForm(request.form) 
    changePasswordForm = ChangePasswordForm(request.form)
    forgotForm = ForgotForm(request.form)
    return loginForm, registerForm, changePasswordForm, forgotForm

@main_blueprint.route('/login', methods=['GET', 'POST'])
def login():
    loginForm, registerForm, changePasswordForm, forgotForm = forms()

    if request.method == 'POST':
        FormType = request.form['FormType']

        if FormType == 'Login':
            if loginForm.validate_on_submit():
                user = User.query.filter_by(email=loginForm.email.data).first()
                if user and bcrypt.check_password_hash(user.password, request.form['password']):
                    if user.confirmed:
                        login_user(user)
                        flash('Welcome!', 'success')
                        time.sleep(0.1)
                        return redirect(url_for('main.home')) 
                    else:
                        userWithoutConfirm = loginForm.email.data
                        clientPymemcache.set('userWithoutConfirm', userWithoutConfirm)
                        return render_template('main/index.html', LoginForm=loginForm, RegisterForm=registerForm, ChangePasswordForm=changePasswordForm, ForgotForm=forgotForm, modal='unconfirmedModal', MsgOutsideModal = False)
                else:
                    flash('Invalid email and/or password. Do you have an account?', 'danger')
                    return render_template('main/index.html', LoginForm=loginForm, RegisterForm=registerForm, ChangePasswordForm=changePasswordForm, ForgotForm=forgotForm, modal='loginModal',  MsgOutsideModal = False)
            else:
                return render_template('main/index.html',  LoginForm=loginForm, RegisterForm=registerForm, ChangePasswordForm=changePasswordForm, ForgotForm=forgotForm, modal='loginModal',  MsgOutsideModal = False)   
        
        if FormType == 'Register':

            if registerForm.validate_on_submit():
                user = User(
                    email=registerForm.email.data,
                    password=registerForm.password.data,
                    confirmed=False)
                db.session.add(user)
                db.session.commit()

                token = generate_confirmation_token(user.email)
                confirm_url = url_for('user.confirm_email', token=token, _external=True)
                html = render_template('user/activate.html', confirm_url=confirm_url)
                subject = "Please confirm your email"
                send_email(user.email, subject, html)

                flash('A confirmation email has been sent.', 'success')
                return redirect(url_for('main.home'))
            else:
                user = User.query.filter_by(email=registerForm.email.data).first()
                if user:
                    flash('Account already registered.', 'success')
                return render_template('main/index.html', LoginForm=loginForm, RegisterForm=registerForm, ChangePasswordForm=changePasswordForm, ForgotForm=forgotForm, modal='registerModal',  MsgOutsideModal = False)

        if FormType == 'Logout':
            logout_user()
            flash('You were logged out.', 'success')
            time.sleep(0.1)
            return redirect(url_for('main.home'))

        if FormType == 'Resend Email':
            userWithoutConfirm = clientPymemcache.get('userWithoutConfirm')
            token = generate_confirmation_token(userWithoutConfirm)
            confirm_url = url_for('user.confirm_email', token=token, _external=True)
            html = render_template('user/activate.html', confirm_url=confirm_url)
            subject = "Please confirm your email"
            send_email(userWithoutConfirm, subject, html)

            flash('A new confirmation email has been sent.', 'success')
            return redirect(url_for('main.home'))
        
        if FormType == 'Recover':
            if forgotForm.validate_on_submit():
                user = User.query.filter_by(email=forgotForm.email.data).first()
                token = generate_confirmation_token(user.email)
                user.password_reset_token = token
                db.session.commit()

                reset_url = url_for('user.forgot_new', token=token, _external=True)
                html = render_template('user/reset.html', username=user.email, reset_url=reset_url)
                subject = "Reset your password"
                send_email(user.email, subject, html)

                flash('A password reset email has been sent.', 'success')

                return redirect(url_for('main.home'))
            else:
                flash('Email not found.', 'danger')
                return render_template('main/index.html',  LoginForm=loginForm, RegisterForm=registerForm, ChangePasswordForm=changePasswordForm, ForgotForm=forgotForm, modal='recoverModal',  MsgOutsideModal = False)

        if FormType == 'Change Password':
            if changePasswordForm.validate_on_submit():   
                if changePasswordForm.userConfirmPassword.data:
                    user = User.query.filter_by(email=changePasswordForm.userConfirmPassword.data).first()
                else:
                    if current_user.is_active():
                        user = User.query.filter_by(email=current_user.email).first()
                    else:
                        flash('Too many tries.', 'danger')
                        return render_template('main/index.html',  LoginForm=loginForm, RegisterForm=registerForm, ChangePasswordForm=changePasswordForm, ForgotForm=forgotForm,  MsgOutsideModal = True)                        
                
                if user:
                    user.password = bcrypt.generate_password_hash(changePasswordForm.password.data)
                    db.session.commit()
                    if user.confirmed:
                        login_user(user)
                        time.sleep(0.1)

                    flash('Password successfully changed.', 'success')
                    return redirect(url_for('main.home'))
                else:
                    flash('Password change was unsuccessful.', 'danger')
                    return render_template('main/index.html',  LoginForm=loginForm, RegisterForm=registerForm, ChangePasswordForm=changePasswordForm, ForgotForm=forgotForm, modal='changePasswordModal',  MsgOutsideModal = False)
            else:
                return render_template('main/index.html',  LoginForm=loginForm, RegisterForm=registerForm, ChangePasswordForm=changePasswordForm, ForgotForm=forgotForm, modal='changePasswordModal',  MsgOutsideModal = False)
    return render_template('main/index.html', LoginForm=loginForm, RegisterForm=registerForm, ChangePasswordForm=changePasswordForm, ForgotForm=forgotForm, MsgOutsideModal = True)
@main_blueprint.route('/', methods=['GET', 'POST'])
def home():
    loginForm, registerForm, changePasswordForm, forgotForm = forms()
    return render_template('main/index.html', LoginForm=loginForm, RegisterForm=registerForm, ChangePasswordForm=changePasswordForm, ForgotForm=forgotForm, MsgOutsideModal = True)

@user_blueprint.route('/confirm/<token>')
def confirm_email(token):
    email = confirm_token(token)
    user = User.query.filter_by(email=email).first()

    if user:
        if user.confirmed:
            flash('Account already confirmed. Please login.', 'success')
        else:
            user.confirmed = True
            user.confirmed_on = datetime.datetime.now()
            db.session.add(user)
            db.session.commit()
            flash('You have confirmed your account.', 'success')
            
    else:
        flash('The confirmation link is invalid or has expired.', 'danger')
       
    return redirect(url_for('main.home'))


@user_blueprint.route('/forgot/new/<token>', methods=['GET', 'POST'])
def forgot_new(token):
    logout_user()
    loginForm, registerForm, changePasswordForm, forgotForm = forms()

    email = confirm_token(token)

    user = User.query.filter_by(email=email).first()
    if user:
        if user.password_reset_token is not None:
            
            if changePasswordForm.validate_on_submit():
                user = User.query.filter_by(email=email).first()
                if user:
                    user.password = bcrypt.generate_password_hash(changePasswordForm.password.data)
                    user.password_reset_token = None
                    db.session.commit()
                    login_user(user)
                    flash('Password successfully changed.', 'success')
                    return redirect(url_for('main.home'))
                else:
                    
                    flash('Password change was unsuccessful.', 'danger')
                    return redirect(url_for('user.change_password'))
            else:
                flash('You can now change your password.', 'success')
                return render_template('main/index.html',  LoginForm=loginForm, RegisterForm=registerForm, ChangePasswordForm=changePasswordForm, ForgotForm=forgotForm, modal='changePasswordModal',  MsgOutsideModal = False, userConfirmPassword = email)
        else:
            flash('Can not reset the password, try again.', 'danger')
    else:
        flash('The confirmation link is invalid or has expired.', 'danger')

    return redirect(url_for('main.home'))


@user_blueprint.route('/admin', methods=['GET', 'POST'])
@login_required
@required_roles
def admin():
	loginForm, registerForm, changePasswordForm, forgotForm = forms()
	databaseForm = DatabaseForm(request.form)
	results = User.query.all()
	table = Results(results)

	if request.method == 'POST':
	    if 'ProBotToShutdown' in request.form:        
	        ProBotToShutdown = request.form['ProBotToShutdown']
	        topic = 'shutdownProBot/' +  ProBotToShutdown
	        client.publish(topic, 'shutdown', qos=0)
	        return render_template('user/admin.html', LoginForm=loginForm, RegisterForm=registerForm, ChangePasswordForm=changePasswordForm, ForgotForm=forgotForm, table=table, AdminPage='ProBotInfo')

	    if 'ChangeUserDatabase' in request.form:
	        if databaseForm.validate_on_submit():
	            user = User.query.filter_by(email=databaseForm.Email.data).first()
	            
	            if not user:
	                OldEmail = clientPymemcache.get('databaseForm.Email.data')
	                user = User.query.filter_by(email=OldEmail).first()

	            user.email = databaseForm.Email.data
	            user.admin = ast.literal_eval(databaseForm.AdminRole.data)
	            user.confirmed = ast.literal_eval(databaseForm.ConfirmedEmail.data)
	            user.probot_control = ast.literal_eval(databaseForm.ControlProBot.data)              
	            db.session.commit()
	        return render_template('user/admin.html', LoginForm=loginForm, RegisterForm=registerForm, ChangePasswordForm=changePasswordForm, ForgotForm=forgotForm, table=table, AdminPage='databaseInfo')	        
            
	return render_template('user/admin.html', LoginForm=loginForm, RegisterForm=registerForm, ChangePasswordForm=changePasswordForm, ForgotForm=forgotForm, table=table, AdminPage='ProBotInfo')

@app.route('/admin/<int:id>', methods=['GET', 'POST'])
@login_required
@required_roles
def edit(id):
    loginForm, registerForm, changePasswordForm, forgotForm = forms()
    databaseForm = DatabaseForm(request.form)

    results = User.query.all()
    table = Results(results)

    DatabaseUser = User.query.filter_by(id=id).first()
    if (DatabaseUser.admin==True):
        databaseForm.AdminRole.default = 'True'
    else:
        databaseForm.AdminRole.default = 'False'

    if (DatabaseUser.confirmed==True):
        databaseForm.ConfirmedEmail.default = 'True'
    else:
        databaseForm.ConfirmedEmail.default = 'False'

    if (DatabaseUser.probot_control==True):
        databaseForm.ControlProBot.default = 'True'
    else:
        databaseForm.ControlProBot.default = 'False'
     
    databaseForm.process()

    databaseForm.Email.data = DatabaseUser.email
    clientPymemcache.set('databaseForm.Email.data', databaseForm.Email.data)

    if DatabaseUser:
        return render_template('user/admin.html', LoginForm=loginForm, RegisterForm=registerForm, ChangePasswordForm=changePasswordForm, ForgotForm=forgotForm, DatabaseForm=databaseForm, modal = 'databaseModal',  table=table, AdminPage='databaseInfo')

@user_blueprint.route('/user', methods=['GET', 'POST'])
@login_required
def user():
	loginForm, registerForm, changePasswordForm, forgotForm = forms()

	if request.method == 'POST':
	    ChosenProBot = request.form['ChosenProBot']

	    clientPymemcache.set('ChosenProBot', ChosenProBot)
	    ProBotChosen = ast.literal_eval(str(clientPymemcache.get('ProBotChosen')))

	    ProBotChosenDict = {sub[0]: sub for sub in ProBotChosen}
	    ProBotInUseDictTimeOutLocal = clientPymemcache.get('ProBotInUseDictTimeOutLocal')
	    ProBotInUseDictTimeOutLocal[ChosenProBot] = time.time()

	    clientPymemcache.set('ProBotInUseDictTimeOutLocal', ProBotInUseDictTimeOutLocal)
        
	    if ProBotChosenDict[ChosenProBot][1]=="Available":
	        ProBotChosenID = [[ChosenProBot, 'NotAvailable']]
	        newsub_dict = {sub[0]: sub for sub in ProBotChosenID}
	        ProBotChosen = [newsub_dict.get(sub[0], sub) for sub in ProBotChosen]
	        clientPymemcache.set('ProBotChosen', ProBotChosen)

	        ip = request.remote_addr 
	        url = 'http://geoip.nekudo.com/api/' + ip
	        
	        r = requests.get(url)
	        js = r.json()
	        
	        for key, value in js.iteritems():
	            if key == 'country':
	                UserIpAddress = [[ChosenProBot, ip + ' ' + js['country']['name'] + ' ' + js['city']]]
	            else:
	                UserIpAddress = [[ChosenProBot, ip + ' ' + 'Not Available']]

	        clientPymemcache.set('UserIpAddress', UserIpAddress)

	        if request.user_agent.platform == ('android' or 'iphone' or 'ipad'): # check which platform we are
	            return render_template('user/active.html', ChosenProBot = ChosenProBot, ControlPage = 'active')
	        else:
	            return render_template('user/active.html', ChosenProBot = ChosenProBot, modal = 'controllerModal', ControlPage = 'active') 
	    else:
	        return render_template('user/user.html', LoginForm=loginForm, RegisterForm=registerForm, ChangePasswordForm=changePasswordForm, ForgotForm=forgotForm, MsgOutsideModal = True)
	return render_template('user/user.html', LoginForm=loginForm, RegisterForm=registerForm, ChangePasswordForm=changePasswordForm, ForgotForm=forgotForm, MsgOutsideModal = True)


@user_blueprint.route('/ResultSearchPhotos', methods=['GET'])
def ResultSearchPhotos():
    return jsonify(listOfFiles =  clientPymemcache.get('listOfFiles')) 

@user_blueprint.route('/ProBotInUse', methods=['POST'])
def ProBotInUse():
    
    ProBotInUseList = ast.literal_eval(json.loads(json.dumps(request.form['ProBotInUse'])))
    ProBotInUseDict = {sub[0]: sub for sub in ProBotInUseList}

    ProBotInUseDictTimeOut = clientPymemcache.get('ProBotInUseDictTimeOut')
    ProBotInUseDictTimeOutLocal = clientPymemcache.get('ProBotInUseDictTimeOutLocal')

    ProBotInUseDictTimeOut[ProBotInUseList[0][0]] = time.time()
    ProBotInUseDictTimeOutLocal[ProBotInUseList[0][0]] = time.time()

    ProBotNotInUse = clientPymemcache.get('ProBotNotInUse')
    ProBotNotInUse[ProBotInUseList[0][0]] = "NotAvailable"

    clientPymemcache.set('ProBotInUseDictTimeOut', ProBotInUseDictTimeOut)
    clientPymemcache.set('ProBotInUseDictTimeOutLocal', ProBotInUseDictTimeOutLocal)    
    clientPymemcache.set('ProBotNotInUse', ProBotNotInUse)

    return b"False"


@cron.interval_schedule(seconds=0.5)
def job_function():
    now = time.time()
    ProBotNotInUse = clientPymemcache.get('ProBotNotInUse')
    ProBotInUseDictTimeOut = clientPymemcache.get('ProBotInUseDictTimeOut')
    ProBotTelemetryDictTimeOut = clientPymemcache.get('ProBotTelemetryDictTimeOut')
    ProBotInUseDictTimeOutLocal = clientPymemcache.get('ProBotInUseDictTimeOutLocal')
    ProBotChosen = ast.literal_eval(str(clientPymemcache.get('ProBotChosen')))
    AllProBotsTelemetryList = ast.literal_eval(str(clientPymemcache.get('AllProBotsTelemetryList')))

    for i in ProBotInUseDictTimeOut:
        if ProBotInUseDictTimeOut[i]:
            if now - ProBotInUseDictTimeOut[i] > 3:
                ProBotNotInUse[i] = "Available"
                ProBotInUseDictTimeOut[i] = None
                
                ProBotChosenID = [[i, 'Available']]
                newsub_dict = {sub[0]: sub for sub in ProBotChosenID}
                ProBotChosen = [newsub_dict.get(sub[0], sub) for sub in ProBotChosen]
        
        if ProBotInUseDictTimeOut[i] == None:
            ProBotNotInUse[i] = "Available"


    for i in ProBotInUseDictTimeOutLocal:
        if ProBotInUseDictTimeOutLocal[i]:
            if now - ProBotInUseDictTimeOutLocal[i] > 3:
                ProBotInUseDictTimeOutLocal[i] = None
                ProBotChosenID = [[i, 'Available']]
                newsub_dict = {sub[0]: sub for sub in ProBotChosenID}
                ProBotChosen = [newsub_dict.get(sub[0], sub) for sub in ProBotChosen]

    for i in ProBotTelemetryDictTimeOut:
        if ProBotTelemetryDictTimeOut[i]:
            if (now - ProBotTelemetryDictTimeOut[i] > 3):
                ProBotTelemetryDictTimeOut[i] = None
                AllProBotsTelemetryDict = [[i, 'Offline']]
                newsub_dict = {sub[0]: sub for sub in AllProBotsTelemetryDict}
                AllProBotsTelemetryList = [newsub_dict.get(sub[0], sub) for sub in AllProBotsTelemetryList]
        else:
                AllProBotsTelemetryDict = [[i, 'Offline']]
                newsub_dict = {sub[0]: sub for sub in AllProBotsTelemetryDict}
                AllProBotsTelemetryList = [newsub_dict.get(sub[0], sub) for sub in AllProBotsTelemetryList]           

    clientPymemcache.set('ProBotChosen', ProBotChosen)      
    clientPymemcache.set('AllProBotsTelemetryList', AllProBotsTelemetryList)           
    clientPymemcache.set('ProBotInUseDictTimeOut', ProBotInUseDictTimeOut)  
    clientPymemcache.set('ProBotTelemetryDictTimeOut', ProBotTelemetryDictTimeOut) 
    clientPymemcache.set('ProBotInUseDictTimeOutLocal', ProBotInUseDictTimeOutLocal) 

    clientPymemcache.set('ProBotNotInUse', ProBotNotInUse)

    return b"False"

@user_blueprint.route('/AddProbot', methods=['GET'])
def AddProbot():
    AllProBotsTelemetryList = ast.literal_eval(str(clientPymemcache.get('AllProBotsTelemetryList')))
    AllProBotsTelemetryDict = {sub[0]: sub for sub in AllProBotsTelemetryList}

    ProBotNotInUse = clientPymemcache.get('ProBotNotInUse')
    ProBotChosen = ast.literal_eval(str(clientPymemcache.get('ProBotChosen')))

    ProBotChosenDict = {sub[0]: sub for sub in ProBotChosen}

    for i in range(1, len(AllProBotsTelemetryList)+1):
        ProBotInUseStatus = AllProBotsTelemetryDict['ProBot' + str(i)]

        if len(ProBotInUseStatus)==2:
            if ProBotInUseStatus[1]=="Offline": 
                Status = 'Offline'
            if ProBotInUseStatus[1]=="NotWorking":
                 Status = 'NotWorking'
        else:
            if ((ProBotInUseStatus[3]=="started")):
                Status = 'Available'
                if ProBotNotInUse:
                    for key, value in ProBotNotInUse.iteritems():
                        if key == 'ProBot' + str(i):
                            if (ProBotNotInUse[key] == "NotAvailable") or (ProBotChosenDict[key][1] == "NotAvailable"):
                                Status = 'NotAvailable'
      
            else:
                Status = 'NotAvailable'
            
        ProBotInUse = [[ProBotInUseStatus[0], Status]]
        newsub_dict = {sub[0]: sub for sub in ProBotInUse}
        
        AllProBotsTelemetryList = [newsub_dict.get(sub[0], sub) for sub in AllProBotsTelemetryList]

    return jsonify(listOfFiles =  [','.join(list) for list in AllProBotsTelemetryList]) 


@user_blueprint.route('/ProBotTelemetry', methods=['GET'])
def ProBotTelemetry():
    ChosenProBot = clientPymemcache.get('ChosenProBot')
    AllProBotsTelemetryList = ast.literal_eval(str(clientPymemcache.get('AllProBotsTelemetryList')))
    AllProBotsTelemetryDict = {sub[0]: sub for sub in AllProBotsTelemetryList}
    if ChosenProBot:
        ChosenProBotTelemetry = [AllProBotsTelemetryDict[ChosenProBot]]
        ChosenProBotTelemetry = str([','.join(list) for list in ChosenProBotTelemetry])
        ChosenProBotTelemetry = ChosenProBotTelemetry.replace("[", "").replace("]", "").replace("'", "")

        return jsonify(ProBotTelemetry =  ChosenProBotTelemetry)
    else:
        return b'False'


@user_blueprint.route('/ProBotTelemetryAdmin', methods=['GET'])
def ProBotTelemetryAdmin():
    AllProBotsTelemetryList = ast.literal_eval(str(clientPymemcache.get('AllProBotsTelemetryList')))
    AllProBotsTelemetryDict = {sub[0]: sub for sub in AllProBotsTelemetryList}
    
    ProBotNotInUse = clientPymemcache.get('ProBotNotInUse')
    ProBotChosen = ast.literal_eval(str(clientPymemcache.get('ProBotChosen')))

    ProBotChosenDict = {sub[0]: sub for sub in ProBotChosen}

    for i in range(1, len(AllProBotsTelemetryList)+1):
        ProBotStatus = AllProBotsTelemetryDict['ProBot' + str(i)]
        if len(ProBotStatus)>2:
            if ((ProBotStatus[3]=="started")):
                Status = 'Available'
                userIp = 'Not Available'
                if ProBotNotInUse:
                    for key, value in ProBotNotInUse.iteritems():
                        if key == 'ProBot' + str(i):
                            #print key, ProBotNotInUse[key]
                            if (ProBotNotInUse[key] == "NotAvailable") or (ProBotChosenDict[key][1] == "NotAvailable"):
                                Status = 'NotAvailable'
                                UserIpAddress = clientPymemcache.get('UserIpAddress')
                                if UserIpAddress:
                                    UserIpAddressDict = {sub[0]: sub for sub in UserIpAddress}
                                    if UserIpAddressDict:
                                            for key, value in UserIpAddressDict.iteritems():
                                                if key == ProBotStatus[0]: 
                                                    userIp = UserIpAddressDict[key][1]
                        else:
                            #print "NO ELSE"
                            #Status = 'Available'
                            userIp = 'Not Available'
            else:
                Status = 'NotAvailable'
                userIp = 'Not Available'
      
            ProBotTelemetry = ProBotStatus + [Status] + [userIp]
            
            AllProBotsTelemetryDict[ProBotTelemetry[0]] = ProBotTelemetry
            AllProBotsTelemetryList = [AllProBotsTelemetryDict.get(sub[0], sub) for sub in AllProBotsTelemetryList]

    return jsonify(listOfFiles =  [','.join(list) for list in AllProBotsTelemetryList])

@user_blueprint.route('/WebpageKeys', methods=['GET', 'POST'])
def WebpageKeys():

    ChosenProBot = str(json.loads(json.dumps(request.form['ChosenProBot'])))
    up = str(json.loads(json.dumps(request.form['up'])))
    down = str(json.loads(json.dumps(request.form['down'])))
    left = str(json.loads(json.dumps(request.form['left'])))
    right = str(json.loads(json.dumps(request.form['right'])))
    ChosenProBot = ChosenProBot.replace('"', "")
    keys = up  + " " + down + " " + left + " " + right          
    topic = 'keys/' +  ChosenProBot
  
    client.publish(topic, keys, qos=0)
        		
    return b"0"
