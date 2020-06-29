from pathlib import Path

from flask import render_template, flash, redirect, url_for, request, send_from_directory
from flask_login import current_user, login_user, logout_user, login_required

from werkzeug.urls import url_parse
from werkzeug.utils import secure_filename

from app import app, db, all_files
from app.forms import LoginForm, RegistrationForm, UploadForm
from app.models import User


@app.route('/', methods=['GET', 'POST'])
@login_required
def index():
    form = UploadForm()
    if form.validate_on_submit():
        files = request.files.getlist('files')
        for file in files:
            filename = secure_filename(file.filename)
            all_files.save(file, folder=current_user.username, name=filename)

        return redirect(url_for('index'))

    user_dir = Path(app.config['UPLOADED_FILES_DEST']) / current_user.username
    user_files = []
    for entry in user_dir.iterdir():
       user_files.append(entry.name)

    return render_template('index.html',
                           title='Upload files', form=form, files=user_files)


@app.route('/download/<filename>')
@login_required
def download(filename):
    user_dir = Path(app.config['UPLOADED_FILES_DEST'] / current_user.username)
    return send_from_directory(user_dir, filename, as_attachment=True)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))

    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))

        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')

        return redirect(next_page)

    return render_template('login.html', title='Sign in', form=form)


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))

    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        user_dir = Path(app.config['UPLOADED_FILES_DEST']) / user.username
        user_dir.mkdir(parents=True, exist_ok=True)

        flash('Congratulations, you now have an account on this shitty site!')
        return redirect(url_for('login'))

    return render_template('register.html', title='Register', form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))
