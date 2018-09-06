# Flask-starter

A starter application template for Flask, with Authentication and User Account.

To run flask-starter locally, you need to:

Step 1: Define some enviromment variables on the project/config/env.cfg.

Step 2: You should be able to run 

	python manage.py runserver and it should run on http://127.0.0.1:5000.


To run flask-starter on the server, we use you [dokku](http://dokku.viewdocs.io/dokku). To deploy the application you need to:


On the server


Step 1: Install dokku

	wget https://raw.githubusercontent.com/dokku/dokku/v0.7.1/bootstrap.sh
	sudo DOKKU_TAG=v0.7.1 bash bootstrap.sh 

or the latest version

Step 2: Create an app

	dokku apps:create <app_name>


On the client


Step1: Add a public key remotely

	cat ~/.ssh/id_rsa.pub | ssh <server_user>@<server_ip> "sudo sshcommand acl-add dokku [description]"

Step 2: Push the apps files to the server

	git remote add dokku dokku@<server_ip>:<app_name>
	git add .
	git commit -a -m "first commit"
	git push dokku master

Step 3: Open the link that is gonna be given where was deployed your application


