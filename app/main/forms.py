from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired, FileAllowed
from wtforms import SubmitField
from werkzeug.utils import secure_filename

from app import user_uploads


class FileUploadForm(FlaskForm):
    files = FileField('Files', validators=[
        FileRequired(),
        FileAllowed(user_uploads, 'Cannot upload scripts nor executables')
    ])
    submit = SubmitField('Upload')
