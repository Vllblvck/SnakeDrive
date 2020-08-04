from pathlib import Path
from flask import request, jsonify, send_from_directory
from werkzeug.utils import secure_filename

from app import db, user_files
from app.models import File
from app.api import bp
from app.api.auth import token_auth
from app.api.errors import bad_request, error_response
from app.helpers.files_helpers import upload_file, edit_file


@bp.route('/files', methods=['POST'])
@token_auth.login_required
def upload_files():
    user = token_auth.current_user()
    if not user.verified:
        return error_response(403, 'Email not confirmed')

    if 'files' not in request.files:
        return bad_request('No files to upload')

    uploaded = []
    errors = []
    files = request.files.getlist('files')
    for file in files:
        file_data = upload_file(user, file)
        if 'error' in file_data:
            errors.append(file_data['error'])
            continue
        file_model = File()
        file_model.from_dict(file_data)
        db.session.add(file_model)
        db.session.commit()
        uploaded.append(file_model.to_dict())

    response = jsonify({'uploaded_files': uploaded, 'errors': errors})
    response.status_code = 201
    return response


@bp.route('/files', methods=['GET'])
@token_auth.login_required
def list_files():
    user = token_auth.current_user()
    if not user.verified:
        return error_response(403, 'Email not confirmed')

    files = File.query.filter_by(user_id=user.id).all()
    response = {'files': []}
    if files:
        files_dict = [file.to_dict() for file in files]
        response['files'] = files_dict
    return response


@bp.route('/files/<filename>', methods=['GET'])
@token_auth.login_required
def download_file(filename):
    user = token_auth.current_user()
    if not user.verified:
        return error_response(403, 'Email not confirmed')

    file = File.query.filter_by(fullname=filename, user_id=user.id).first()
    if not file:
        return error_response(404, 'File {} does not exist'.format(filename))
    return send_from_directory(user.get_dir(), file.fullname, as_attachment=True)


@bp.route('files/<filename>', methods=['PUT'])
@token_auth.login_required
def edit_file(filename):
    user = token_auth.current_user()
    if not user.verified:
        return error_response(403, 'Email not confirmed')

    data = request.get_json() or {}
    if 'name' not in data:
        return bad_request('Must include name field')

    file = File.query.filter_by(fullname=filename, user_id=user.id).first()
    if not file:
        return error_response(404, 'File {} doest not exist'.format(filename))

    file_data = edit_file(user, file, data['name'])
    file.from_dict(file_data)
    db.session.commit()
    response = jsonify(file.to_dict())
    response.status_code = 201
    return response


@bp.route('files/<filename>', methods=['DELETE'])
@token_auth.login_required
def delete_file(filename):
    user = token_auth.current_user()
    if not user.verified:
        return error_response(403, 'Email not confirmed')

    file = File.query.filter_by(fullname=filename, user_id=user.id).first()
    if not file:
        return error_response(404, 'File {} does not exist'.format(filename))

    filepath = Path(file.path)
    filepath.unlink()
    db.session.delete(file)
    db.session.commit()
    return '', 204
