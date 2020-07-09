from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_uploads import configure_uploads, patch_request_class, UploadSet, AllExcept, SCRIPTS, EXECUTABLES
from flask_mail import Mail

from config import Config


db = SQLAlchemy()
migrate = Migrate()
mail = Mail()
user_files = UploadSet('files', AllExcept(SCRIPTS + EXECUTABLES))


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    migrate.init_app(app, db)
    mail.init_app(app)
    configure_uploads(app, (user_files))
    patch_request_class(app, 1 * 1024 * 1024 * 1024)

    from app.api import bp as api_bp
    app.register_blueprint(api_bp, url_prefix='/api')
    
    from app.errors import bp as errors_bp
    app.register_blueprint(errors_bp, url_prefix='/error')

    from app.email import bp as email_bp
    app.register_blueprint(email_bp, url_prefix='/email')

    return app


from app import models
