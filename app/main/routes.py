from flask import render_template, redirect
from flask_login import login_required, current_user

from app.main import bp


@bp.route('/')
@login_required
def index():
    if current_user.verified != True:
        return render_template('main/unverified.html')
    
    return render_template('main/index.html')


@bp.route('/welcome')
def welcome():
    return render_template('main/welcome.html')
