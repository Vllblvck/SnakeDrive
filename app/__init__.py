from flask import Flask, session
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_uploads import configure_uploads, UploadSet, AllExcept, SCRIPTS, EXECUTABLES

from config import Config
from app import routes, models

app = Flask(__name__)
app.config.from_object(Config)

db = SQLAlchemy(app)
migrate = Migrate(app, db)

login = LoginManager(app)
login.login_view = 'login'

all_files = UploadSet('files', AllExcept(SCRIPTS + EXECUTABLES))
configure_uploads(app, (all_files))
