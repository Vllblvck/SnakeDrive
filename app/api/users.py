from flask import jsonify, url_for, request

from app import db
from app.email.emails import send_verification_email
from app.models import User
from app.helpers import delete_folder, valid_email, valid_username
from app.api import bp
from app.api.auth import token_auth
from app.api.errors import bad_request, error_response


@bp.route('/users', methods=['GET'])
@token_auth.login_required
def get_user():
    return token_auth.current_user().to_dict()


@bp.route('/users', methods=['POST'])
def create_user():
    data = request.get_json() or {}
    if 'username' not in data or 'email' not in data or 'password' not in data:
        return bad_request('Must include username, email and password fields!')

    if User.query.filter_by(username=data['username']).first() or \
            not valid_username(data['username']):
        return bad_request('Data must contain valid username')

    if User.query.filter_by(email=data['email']).first() or \
            not valid_email(data['email']):
        return bad_request('Data must contain valid email')

    user = User()
    user.from_dict(data, new_user=True)
    db.session.add(user)
    db.session.commit()
    send_verification_email(user)
    response = jsonify(user.to_dict())
    response.status_code = 201
    return response


@bp.route('/users', methods=['PUT'])
@token_auth.login_required
def edit_user():
    user = token_auth.current_user()
    data = request.get_json() or {}
    if 'username' in data and data['username'] == user.username or \
            not valid_username(data['username']):
        return bad_request('Data must contain valid username')
    
    if 'email' in data and data['email'] == user.email or \
            not valid_email(data['email']):
        return bad_request('Data must containt valid email')
    
    user.from_dict(data)
    if 'email' in data:
        user.verified = False
        send_verification_email(user)
    db.session.commit()
    return user.to_dict()

#TODO email confirmation ?
@bp.route('/users', methods=['DELETE'])
@token_auth.login_required
def delete_user():
    user = token_auth.current_user()
    delete_folder(user.get_dir())
    db.session.delete(user)
    db.session.commit()
    return '', 204
