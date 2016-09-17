"""Forms.py."""
from wtforms import Form, PasswordField, TextField, RadioField, validators


class RegistrationForm(Form):
    """Registration form."""

    username = TextField(
        (u'What do you want us to call you?'),
        [validators.Length(min=3, max=15), validators.Required()]
    )
    email = TextField(
        (u'Email Address'), [validators.Length(min=6, max=35)]
    )
    password = PasswordField((u'Password'), [
        validators.Required(),
        validators.EqualTo(
            u'confirm', message=(u'Passwords must match')
        ),
        validators.Length(min=6, max=16)
    ])
    confirm = PasswordField((u'Repeat Password'))


class LoginForm(Form):
    """Login Form."""

    email = TextField(
        (u'Email Address'), [validators.Length(min=6, max=35)]
    )
    password = PasswordField((u'Password'), [
        validators.Required(),
    ])


class ResetPasswordForm(Form):
    """Reset Password Form."""

    email = TextField(
        (u'Email Address'), [validators.Length(min=6, max=35)]
    )


class ConfirmResetPasswordForm(Form):
    """Reset Password Form."""

    password = PasswordField((u'Password'), [
        validators.Required(),
        validators.EqualTo(
            u'confirm', message=(u'Passwords must match')
        ),
        validators.Length(min=6, max=16)
    ])
    confirm = PasswordField((u'Repeat Password'))
    
    
class SelectProBotForm(Form):
	
	probot = RadioField(u'Choose one:', validators = [validators.Required()], choices=[], coerce=int)
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
