from flask import render_template, flash, redirect, url_for, request
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.urls import url_parse

from app import db
from app.auth import bp
from app.auth.forms import LoginForm, RegistrationForm, ResetPasswordRequestForm, ResetPasswordForm
from app.models import User
from app.email import send_verification_email, send_password_reset_email


@bp.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.drive'))

    form = RegistrationForm()
    if form.validate_on_submit():
        user_data = {
            'username': form.username.data,
            'email': form.email.data,
            'password': form.password.data
        }
        user = User()
        user.from_dict(user_data, new_user=True)
        db.session.add(user)
        db.session.commit()
        send_verification_email(user)
        flash('Registration successfull, please verify your email')
        return redirect(url_for('auth.login'))

    return render_template('auth/register.html', form=form)


@bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.drive'))

    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if not user or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('auth.login'))

        login_user(user, remember=form.remember.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('main.drive')
        return redirect(next_page)

    return render_template('auth/login.html', form=form)


@bp.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))


@bp.route('/verify_email', methods=['GET', 'POST'])
@login_required
def verify_email_request():
    if current_user.verified:
        return redirect(url_for('main.drive'))

    send_verification_email(current_user)
    return render_template('auth/verify_email_request.html')


@bp.route('/verify_email/<token>', methods=['GET', 'POST'])
def verify_email(token):
    if current_user.verified:
        return redirect(url_for('main.drive'))

    user = User.check_jwt_token(token)
    if not user:
        return render_template('auth/invalid_token.html')
    user.verified = True
    db.session.commit()
    return render_template('auth/verify_email.html')


@bp.route('/reset_password', methods=['GET', 'POST'])
def reset_password_request():
    if current_user.is_authenticated:
        return redirect(url_for('main.drive'))

    form = ResetPasswordRequestForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if not user:
            flash('User with given email doesn\'t exist')
            return redirect(url_for('auth.reset_password_request'))

        send_password_reset_email(user)
        flash('Password resent link was sent to you')
        return redirect(url_for('auth.login'))

    return render_template('auth/reset_password_request.html', form=form)


@bp.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    if current_user.is_authenticated:
        return redirect(url_for('main.drive'))

    user = User.check_jwt_token(token)
    if not user:
        return render_template('auth/invalid_token.html')

    form = ResetPasswordForm()
    if form.validate_on_submit():
        user.set_password(form.password.data)
        db.session.commit()
        flash('Your password has been reset')
        return redirect(url_for('auth.login'))

    return render_template('auth/reset_password.html', form=form)
