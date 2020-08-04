import pathlib
from flask import render_template, redirect, url_for, request, current_app, flash, send_from_directory
from flask_login import login_required, current_user

from app import user_files, db
from app.main import bp
from app.main.forms import FileUploadForm
from app.models import File
from app.helpers.files_helpers import upload_file, edit_file


@bp.route('/welcome', methods=['GET'])
def welcome():
    if current_user.is_authenticated:
        return redirect(url_for('main.drive'))

    return render_template('main/welcome.html')


@bp.route('/', methods=['GET', 'POST'])
@login_required
def drive():
    if not current_user.verified:
        return render_template('main/unverified.html')

    form = FileUploadForm()
    if form.validate_on_submit():
        errors = []
        files = request.files.getlist('files')
        for file in files:
            file_data = upload_file(current_user, file)
            if 'error' in file_data:
                errors.append(file_data['error'])
                continue
            file_model = File()
            file_model.from_dict(file_data)
            db.session.add(file_model)
            db.session.commit()

        for error in errors:
            flash(error)

        return redirect(url_for('main.drive'))

    files = File.query.filter_by(user_id=current_user.id).all()
    print(files)
    return render_template('main/drive.html', form=form, files=files)


@bp.route('/download_file/<filename>')
@login_required
def download_file(filename):
    if not current_user.verified:
        return render_template('main/unverified.html')

    file = File.query.filter_by(
        fullname=filename, user_id=current_user.id).first_or_404()

    dir = current_user.get_dir()
    return send_from_directory(dir, filename, as_attachment=True)


@bp.route('/delete_file/<filename>')
@login_required
def delete_file(filename):
    if not current_user.verified:
        return render_template('main/unverified.html')

    file = File.query.filter_by(
        fullname=filename, user_id=current_user.id).first_or_404()

    filepath = pathlib.Path(file.path)
    filepath.unlink()
    db.session.delete(file)
    db.session.commit()
    return redirect(url_for('main.drive'))


@bp.route('/edit_file/<filename>')
@login_required
def edit_file(filename):
    if not current_user.verified:
        return render_template('main/unverified.html')

    file = File.query.filter_by(
        fullname=filename, user_id=current_user.id).first_or_404()

    #TODO implement edit file form or something
    #TODO make below code work
    # new_name = 'hardcoded'
    # file_data = edit_file(current_user, file, new_name)
    # file.from_dict(file_data)
    # db.session.commit()

    return redirect(url_for('main.drive'))
