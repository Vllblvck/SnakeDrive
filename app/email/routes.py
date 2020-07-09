from flask import render_template, abort

from app import db
from app.email import bp
from app.email.emails import send_verification_email
from app.models import User


@bp.route('/verify_email/<token>', methods=['GET', 'POST'])
def verify_email(token):
    user = User.check_email_verification_token(token)
    if not user:
        return render_template('email/invalid_verification_token.html')
    user.verified = True
    db.session.commit()
    return render_template('email/success_verification.html')
