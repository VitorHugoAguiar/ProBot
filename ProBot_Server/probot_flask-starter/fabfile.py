#!flask/bin/python

"""
fabfile.py.

This file configures and controls remote operations on the
Staging and Production servers.
"""
from fabric.api import *

# declare our hosts
staging_server = ''
production_server = ''

############################
# Reusable base operations #
############################
def restart_celery():
    """Base restart celery operation."""
    env.user = 'root'
    run("sudo restart celery")


##############################
# Server-specific operations #
##############################

def staging():
    """Set host server to Staging."""
    env.host_string = staging_server


def production():
    """Set host server to Staging."""
    env.host_string = production_server


def deploy_master():
    """Base deploy operation."""
    env.user = 'rivals'
    with cd("flask-starter/"):
        run("git pull origin master")
    # change to root
    env.user = 'root'
    run("sudo restart gunicorn")


def deploy_dev():
    """Base deploy operation."""
    env.user = 'rivals'
    with cd("flask-starter/"):
        run("git pull origin sam_dev")
    # change to root
    env.user = 'root'
    run("sudo restart gunicorn")


def restart_celery_staging():
    """Restart Celery on Staging via Upstart."""
    env.host_string = staging_server
    restart_celery(branch="dev")


def restart_celery_production():
    """Restart Celery on Production via Upstart."""
    env.host_string = staging_server
    restart_celery(branch="master")


def provision_server(username=None):
    """Provision an ubuntu server."""
    db_name = 'flaskstarter'
    env.user = 'root'
    run('sudo apt-get update')
    run('sudo apt-get install python-pip python-dev libpq-dev postgresql postgresql-contrib nginx git')
    #  Add environment variables to /etc/environment
    #  TODO: add vars
    run('touch /etc/environment')
    #  Add user
    run('adduser {}'.format(username))
    #  setup db
    run('psql -U postgres -c "CREATE ROLE {0} WITH PASSWORD \'{1}\' NOSUPERUSER CREATEDB NOCREATEROLE LOGIN;"'.format(username, 'pass'))
    run('psql -U postgres -c "CREATE DATABASE {0} WITH OWNER={1} TEMPLATE=template0 ENCODING=\'utf-8\';"'.format(db_name, username))
    #  exit
    run('exit')
    #  change to user
    env.user = username
    #  Make virtualenv and activate it
    run('virtualenv env')
    run('source env/bin/activate')
    run('git clone git@github.com:samgclarke/flask-starter.git')
    run('pip install -r flask-starter/requirements.txt')
    #  TODO:
    #  gunicorn upstart
    #  upgrade db


######################
#  LOCAL OPERATIONS  #
######################

def unit_tests():
    """Run python unit tests locally."""
    with cd('~/flask-projects/flask-starter/'):
        local("export APP_SETTINGS='config.TestingConfig'")
        local('python tests.py')
        local("export APP_SETTINGS='config.DevelopmentConfig'")


def protractor_tests():
    """Run protractor tests locally."""
    with cd('~/flask-projects/flask-starter/'):
        local("export APP_SETTINGS='config.TestingConfig'")
        with settings(warn_only=True):
            local('rm tests.db')
        local('python db_create.py')
        local('python db_populate.py')
        local('python runserver.py &')
        local('gulp protractor')
        local('rm tests.db')
        #  reset config
        local("export APP_SETTINGS='config.DevelopmentConfig'")
