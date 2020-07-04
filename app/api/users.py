from flask import jsonify, url_for, request, abort

from app import db
from app.models import User
from app.api import bp
from app.api.auth import token_auth
from app.api.errors import bad_request, error_response


@bp.route('/users/<int:id>', methods=['GET'])
@token_auth.login_required
def get_user(id):
    if token_auth.current_user().id != id:
        return error_response(403, 'You don\'t have permission for this account')
    return jsonify(User.query.get_or_404(id).to_dict())

# Email verification and password requirements
@bp.route('/users', methods=['POST'])
def create_user():
    data = request.get_json() or {}
    if 'username' not in data or 'email' not in data or 'password' not in data:
        return bad_request('Must include username, email and password fields!')
    if User.query.filter_by(username=data['username']).first():
        return bad_request('Data must contain valid username')
    if User.query.filter_by(email=data['email']).first():
        return bad_request('Data must contain valid email')
    
    user = User()
    user.from_dict(data, new_user=True)
    db.session.add(user)
    db.session.commit()
    response = jsonify(user.to_dict())
    response.status_code = 201
    response.headers['Location'] = url_for('api.get_user', id=user.id)
    return response


@bp.route('/users/<int:id>', methods=['PUT'])
@token_auth.login_required
def update_user(id):
    if token_auth.current_user().id != id:
        return error_response(403, 'You don\'t have permission for this account')
    user = User.query.get_or_404(id)
    data = request.get_json() or {}
    if 'username' in data and data['username'] != user.username and \
            User.query.filter_by(username=data['username']).first():
        return bad_request('Data must contain valid username')
    if 'email' in data and data['email'] != user.email and \
            User.query.filter_by(email=data['email']).first():
        return bad_request('Data must containt valid email')

    user.from_dict(data)
    db.session.commit()
    return jsonify(user.to_dict())