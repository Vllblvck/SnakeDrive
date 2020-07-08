from pathlib import Path
from flask import request, jsonify, send_from_directory
from werkzeug.utils import secure_filename

from app import db, user_files
from app.models import File
from app.api import bp
from app.api.auth import token_auth
from app.api.errors import bad_request, error_response


@bp.route('/files', methods=['POST'])
@token_auth.login_required
def upload_files():
    user = token_auth.current_user()
    if not user.verified:
        return error_response(403, 'Email not confirmed')

    if 'files' not in request.files:
        return bad_request('No files to upload')

    files = request.files.getlist('files')
    user_dir = user.get_dir()
    uploaded = []
    errors = []
    for file in files:
        filename = secure_filename(file.filename)
        if not user_files.file_allowed(file, filename):
            errors.append(filename + ' has forbidden extension')
            continue
        file_path = user_dir / filename
        if file_path.exists():
            filename = user_files.resolve_conflict(user_dir, filename)
            file_path = user_dir / filename
        user_files.save(file, folder=str(user.id), name=filename)
        file_data = {
            'name': file_path.stem,
            'extension': file_path.suffix,
            'fullname': filename,
            'size': file_path.stat().st_size,
            'path': str(file_path),
            'user_id': user.id
        }
        db_data = File()
        db_data.from_dict(file_data)
        db.session.add(db_data)
        db.session.commit()
        uploaded.append(db_data.to_dict())

    response_content = {
        'uploaded_files': uploaded,
        'errors': errors
    }
    response = jsonify(response_content)
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

    name = secure_filename(data['name'])
    fullname = name + file.extension
    path = user.get_dir() / fullname
    file_data = {
        'name': name,
        'fullname': fullname,
        'path': str(path)
    }

    old_path = Path(file.path)
    old_path.rename(path.with_name(fullname))
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
