from flask import render_template, redirect
from flask_login import login_required, current_user

from app.main import bp
from app.main.forms import FileUploadForm


@bp.route('/')
@login_required
def drive():
    if current_user.verified != True:
        return render_template('main/unverified.html')
    
    form = FileUploadForm()
    if form.validate_on_submit():
        pass 

    return render_template('main/drive.html')


@bp.route('/welcome')
def welcome():
    return render_template('main/welcome.html')
