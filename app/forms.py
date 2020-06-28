from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired, FileAllowed
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Email, EqualTo, ValidationError
from flask_uploads import UploadSet, AllExcept, SCRIPTS, EXECUTABLES

from app.models import User


ALLOWED_FILES = UploadSet('Files', AllExcept(SCRIPTS + EXECUTABLES))


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember me')
    submit = SubmitField('Sign in')


class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField(
            'Reapeat password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('User {} already exists!'.format(username.data))

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Account for {} already exists!'.format(email.data))


class UploadForm(FlaskForm):
    upload = FileField('File', validators=[
        FileRequired(),
        FileAllowed(ALLOWED_FILES, 'No executables or scripts!')
        ])
    submit = SubmitField('Upload')
