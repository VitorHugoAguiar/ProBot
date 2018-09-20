from flask_table import Table, Col, LinkCol
 
class Results(Table):
    id = Col('Id', show=False)
    email = Col('Email')
    password = Col('Password', show=False)
    registered_on = Col('Registered Date', show=False)
    admin = Col('Admin Role', show=False)
    confirmed = Col('Confirmed Email', show=False)
    confirmed_on = Col('Confirmation Date', show=False)
    password_reset_token = Col('Password Reset Token', show=False)
    probot_control = Col('Can control a ProBot?')
    edit = LinkCol('Edit', 'edit', url_kwargs=dict(id='id'))
