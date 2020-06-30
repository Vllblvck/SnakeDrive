from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired, FileAllowed

from wtforms import SubmitField 

from app import all_files


class UploadForm(FlaskForm):
    files = FileField('Files', render_kw={'multiple': True},
                      validators=[
        FileRequired(),
        FileAllowed(all_files, 'No scripts nor executables!')
    ])
    submit = SubmitField('Upload')
