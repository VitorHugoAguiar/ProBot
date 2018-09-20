# project/user/forms.py


from flask_wtf import FlaskForm
from wtforms import TextField, PasswordField, HiddenField, RadioField
from wtforms.validators import DataRequired, Email, Length, EqualTo

from project.models import User


class LoginForm(FlaskForm):
    email = TextField('email', validators=[DataRequired(), Email()])
    password = PasswordField('password', validators=[DataRequired()])


class RegisterForm(FlaskForm):
    email = TextField(
        'email',
        validators=[DataRequired(), Email(message=None), Length(min=6, max=255)])
    password = PasswordField(
        'password',
        validators=[DataRequired(), Length(min=6, max=255)]
    )
    confirm = PasswordField(
        'Repeat password',
        validators=[
            DataRequired(),
            EqualTo('password', message='Passwords must match.')
        ]
    )

    def validate(self):
        initial_validation = super(RegisterForm, self).validate()
        if not initial_validation:
            return False
        user = User.query.filter_by(email=self.email.data).first()
        if user:
            self.email.errors.append("Email already registered")
            return False
        return True


class ForgotForm(FlaskForm):
    email = TextField(
        'email',
        validators=[DataRequired(), Email(message=None), Length(min=6, max=255)])

    def validate(self):
        initial_validation = super(ForgotForm, self).validate()
        if not initial_validation:
            return False
        user = User.query.filter_by(email=self.email.data).first()
        if not user:
            self.email.errors.append("This email is not registered")
            return False
        return True


class ChangePasswordForm(FlaskForm):
    password = PasswordField(
        'password',
        validators=[DataRequired(), Length(min=6, max=255)]
    )
    confirm = PasswordField(
        'Repeat password',
        validators=[
            DataRequired(),
            EqualTo('password', message='Passwords must match.')
        ]
    )
    userConfirmPassword = HiddenField()

class DatabaseForm(FlaskForm):
    Email = TextField('Email')
    AdminRole = RadioField('AdminRole', choices=[('True','True'),('False','False')])
    ConfirmedEmail = RadioField('ConfirmedEmail', choices=[('True','True'),('False','False')])
    ControlProBot = RadioField('ControlProBot', choices=[('True','True'),('False','False')])

    