"""Forms.py."""
from wtforms import Form, PasswordField, TextField, RadioField, validators, SelectField, HiddenField, TextAreaField, SubmitField, ValidationError

class ContactForm(Form):
  name = TextField("Name",  [validators.Required("Please enter your name.")])
  email = TextField("Email",  [validators.Required("Please enter your email address."), validators.Email("Please enter your email address.")])
  subject = TextField("Subject",  [validators.Required("Please enter a subject.")])
  message = TextAreaField("Message",  [validators.Required("Please enter a message.")])
  submit = SubmitField("Send")


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
    
    
class TestForm(Form):
  fld1 = TextField("")
	
	
	
	
	
	
	
	
	
	
	
	
	
	
