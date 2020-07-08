import os
import jwt
import base64
from time import time
from pathlib import Path
from datetime import datetime, timedelta

from flask import url_for, current_app
from werkzeug.security import generate_password_hash, check_password_hash

from app import db


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), index=True, unique=True, nullable=False)
    username = db.Column(db.String(64), index=True, unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    token = db.Column(db.String(32), index=True, unique=True)
    token_expiration = db.Column(db.DateTime)
    verified = db.Column(db.Boolean, default=False)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def get_token(self, expires_in=3600):
       now = datetime.utcnow()
       if self.token and self.token_expiration > now + timedelta(seconds=60):
           return self.token
       self.token = base64.b64encode(os.urandom(24)).decode('utf-8')
       self.token_expiration = now + timedelta(seconds=expires_in)
       db.session.add(self)
       return self.token

    def revoke_token(self):
        self.token_expiration = datetime.utcnow() - timedelta(seconds=1)

    @staticmethod
    def check_token(token):
        user = User.query.filter_by(token=token).first()
        if user is None or user.token_expiration < datetime.utcnow():
            return None
        return user

    def get_email_verification_token(self, expires_in=3600):
        return jwt.encode(
            {'verify_email': self.id, 'exp': time() + expires_in},
            current_app.config['SECRET_KEY'],
            algorithm='HS256'
        ).decode('utf-8')

    @staticmethod
    def check_email_verification_token(token):
        try:
            id = jwt.decode(token, current_app.config['SECRET_KEY'],
                            algorithms=['HS256'])['verify_email']
        except:
            return
        return User.query.get(id)

    def get_dir(self):
        dir = Path(current_app.config['UPLOADED_FILES_DEST']) / str(self.id)
        dir.mkdir(parents=True, exist_ok=True)
        return dir

    def to_dict(self):
        data = {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'verified': self.verified,
        }
        return data

    def from_dict(self, data, new_user=False):
        for field in ['username', 'email', 'verified']:
            if field in data:
                setattr(self, field, data[field])
        if new_user and 'password' in data:
            self.set_password(data['password'])


class File(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), index=True, nullable=False)
    extension = db.Column(db.String(10), nullable=False)
    fullname = db.Column(db.String(130), index=True, nullable=False)
    size = db.Column(db.String(120), nullable=False)
    path = db.Column(db.String(120), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey(
        'user.id'), index=True, nullable=False)

    def to_dict(self, path=False):
        data = {
            'id': self.id,
            'name': self.name,
            'extension': self.extension,
            'fullname': self.fullname,
            'size': self.size,
            'user_id': self.user_id,
        }
        if path:
            data['path'] = self.path
        return data

    def from_dict(self, data):
        for field in ['name', 'extension', 'fullname', 'size', 'path', 'user_id']:
            if field in data:
                setattr(self, field, data[field])
