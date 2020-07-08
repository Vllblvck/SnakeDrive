from threading import Thread
from flask import current_app, render_template
from flask_mail import Message

from app import mail


def send_async_email(msg):
    with current_app:
        mail.send(msg)
    

def send_email(subject, sender, recipients, text_body, html_body):
    msg = Message(subject, sender=sender,
                  recipients=recipients)
    msg.body = text_body
    msg.html = html_body
    # Thread(target=send_async_email, args=(msg)).start()
    mail.send(msg)


def send_verification_email(user):
    token = user.get_email_verification_token()
    send_email(
        subject='[SnakeDrive] Confirm your email address',
        sender=current_app.config['APP_MAIL'],
        recipients=[user.email],
        text_body=render_template(
            'verify_email.txt', user=user, token=token),
        html_body=render_template(
            'verify_email.html', user=user, token=token)
    )