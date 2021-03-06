from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired, FileAllowed
from wtforms import SubmitField
from werkzeug.utils import secure_filename

from app import user_files


class FileUploadForm(FlaskForm):
    files = FileField('', validators=[
        FileRequired('No files to upload'),
        FileAllowed(user_files, 'Cannot upload scripts nor executables')
    ], render_kw={'multiple': True})
    submit = SubmitField('Upload')
