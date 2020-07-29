from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_uploads import configure_uploads, patch_request_class, UploadSet, AllExcept, SCRIPTS, EXECUTABLES
from flask_mail import Mail

from config import Config


db = SQLAlchemy()
migrate = Migrate()
login_manager = LoginManager()
mail = Mail()
user_files = UploadSet('files', AllExcept(SCRIPTS + EXECUTABLES))


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    mail.init_app(app)
    configure_uploads(app, (user_files))
    patch_request_class(app, 1 * 1024 * 1024 * 1024)

    from app.main import bp as main_bp
    app.register_blueprint(main_bp)

    from app.auth import bp as auth_bp
    app.register_blueprint(auth_bp)

    from app.api import bp as api_bp
    app.register_blueprint(api_bp, url_prefix='/api')
    
    from app.errors import bp as errors_bp
    app.register_blueprint(errors_bp, url_prefix='/error')
    
    return app


from app import models, email, helpers
