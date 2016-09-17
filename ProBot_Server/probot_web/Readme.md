# flask-starter

A starter application template for Flask, with Authentication and User Account.

To run flask-starter locally, you need to:

Step 1: Define some enviromment variables:

	export APP_SETTINGS="config.DevelopmentConfig"
	export DATABASE_URL=$PWD
	export CONTACT_EMAIL=YOUR@GMAIL
	export LOGGING_URL=localhost:514
	export APP_MAIL_USERNAME=YOURGMAILUSERNAME
	export APP_MAIL_PASSWORD=YOURGMAILPASS

Step 2: Then in the flask-starter directory, you need to set up the database. Basically, this means getting the database to create the appropriate tables in the database as represented in models.py

	python manage.py db init
	python manage.py db migrate
	python manage.py db upgrade


Step 3: You should be able to run 

	python manage.py runserver and it should run on http://127.0.0.1:5000.


To run flask-starter on the server, we use you [dokku](http://dokku.viewdocs.io/dokku). To deploy the application. you need to:


On the server


Step 1: Install dokku

	wget https://raw.githubusercontent.com/dokku/dokku/v0.7.1/bootstrap.sh
	sudo DOKKU_TAG=v0.7.1 bash bootstrap.sh 


Step 2: Create an app

	dokku apps:create <app_name>


Step 3: Make a persistent storage an give the right permissions

	sudo mkdir -p  /var/lib/dokku/data/<app_name_storage>
	sudo chown -R dokku:dokku /var/lib/dokku/data/<app_name_storage>
	sudo chown -R 32767:32767 /var/lib/dokku/data/<app_name_storage>
	sudo chmod a+rw /var/lib/dokku/data/<app_name_storage>
	dokku storage:mount probot /var/lib/dokku/data/<app_name_storage>:/storage


Step 4: Config the enviromment variables

	dokku config:set <app_name> APP_SETTINGS="config.DevelopmentConfig" DATABASE_URL="/storage/__database.db" CONTACT_EMAIL=YOUR@GMAIL LOGGING_URL=localhost:514 APP_MAIL_USERNAME=YOURGMAILUSERNAME APP_MAIL_PASSWORD=YOURGMAILPASS


Step 5: Create the database

	dokku run <app_name_storage> python manage.py db init    --directory '/storage/migrations'
	dokku run <app_name_storage> python manage.py db migrate --directory '/storage/migrations'
	dokku run <app_name_storage> python manage.py db upgrade --directory '/storage/migrations'


On the client


Step1: Add a public key remotely

	cat ~/.ssh/id_rsa.pub | ssh <server_user>@<server_ip> "sudo sshcommand acl-add dokku [description]"

Step 2: Push the apps files to the server

	git remote add dokku dokku@<server_ip>:<app_name>
	git add .
	git commit -a -m "first commit"
	git push dokku master

Step 3: Open the link that is gonna be given where was deployed your application


Finally, you need to run  [Crossbar.io](https://github.com/VitorHugoAguiar/ProBot/tree/master/ProBot_Server/probot_server/.crossbar).
