from pathlib import Path

from flask import render_template, redirect, url_for, request, send_from_directory, current_app
from flask_login import current_user, login_required

from werkzeug.utils import secure_filename

from app import db, all_files
from app.main import bp
from app.main.forms import UploadForm 


@bp.route('/', methods=['GET', 'POST'])
@login_required
def index():
    form = UploadForm()
    if form.validate_on_submit():
        files = request.files.getlist('files')
        for file in files:
            filename = secure_filename(file.filename)
            all_files.save(file, folder=current_user.username, name=filename)

        return redirect(url_for('main.index'))

    user_dir = Path(current_app.config['UPLOADED_FILES_DEST']) / current_user.username
    user_files = []
    for entry in user_dir.iterdir():
       user_files.append(entry.name)

    return render_template('index.html',
                           title='Upload files', form=form, files=user_files)


@bp.route('/download/<filename>')
@login_required
def download(filename):
    user_dir = Path(current_app.config['UPLOADED_FILES_DEST']) / current_user.username
    return send_from_directory(user_dir, filename, as_attachment=True)
