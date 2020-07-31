from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo, Length

from app.models import User
from app.helpers import valid_username


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember me')
    submit = SubmitField('Sign In')


class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[
        DataRequired(),
        Length(min=1, max=32,
               message='Username must be between 1 and 32 characters')
    ])
    email = StringField('Email', validators=[
        DataRequired(),
        Email('Invalid email address'),
        Length(max=320,
            message='Email should have 320 characters max')
    ])
    password = PasswordField('Password', validators=[
        DataRequired(),
        Length(max=32, message='Password can\'t have more than 32 characters')
    ])
    password_repeat = PasswordField('Repeat password', validators=[
        DataRequired(),
        EqualTo('password')
    ])
    submit = SubmitField('Sign up')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('Username is taken')
        elif not valid_username(username.data):
            raise ValidationError('Username can\'t contain special characters')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('Email is taken')


class ResetPasswordRequestForm(FlaskForm):
    email = StringField('Email', validators=[
        DataRequired(),
        Email('Invalid email address')
    ])
    submit = SubmitField('Send email')


class ResetPasswordForm(FlaskForm):
    password = PasswordField('New password', validators=[
        DataRequired(),
        Length(max=32, message='Password can\'t have more than 32 characters')
    ])
    password_repeat = PasswordField('Repeat password', validators=[
        DataRequired(),
        EqualTo('password')
    ])
    submit = SubmitField('Change')
