from threading import Thread
from flask import current_app, render_template
from flask_mail import Message

from app import mail


def send_async(app, msg):
    with app.app_context():
        mail.send(msg)


def send_email(subject, sender, recipients, text_body, html_body):
    if not current_app.config['MAIL_SERVER']:
        return

    msg = Message(subject, sender=sender,
                  recipients=recipients)
    msg.body = text_body
    msg.html = html_body

    app = current_app._get_current_object()
    Thread(target=send_async, args=(app, msg)).start()


def send_verification_email(user):
    token = user.get_email_token()
    send_email(
        subject='[SnakeDrive] Confirm your email address',
        sender=current_app.config['APP_MAIL'],
        recipients=[user.email],
        text_body=render_template(
            'email/verify_email.txt', user=user, token=token),
        html_body=render_template(
            'email/verify_email.html', user=user, token=token)
    )


def send_password_reset_email(user):
    token = user.get_email_token(expires_in=900)
    send_email(
        subject='[SnakeDrive] Reset your password',
        sender=current_app.config['APP_MAIL'],
        recipients=[user.email],
        text_body=render_template(
            'email/reset_password.txt', user=user, token=token),
        html_body=render_template(
            'email/reset_password.html', user=user, token=token)
    )
