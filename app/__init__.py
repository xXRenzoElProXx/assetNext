from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager

# Inicialización sin app

db = SQLAlchemy()
migrate = Migrate()

app = Flask(__name__)
app.config.from_pyfile('../config.py')
app.secret_key = 'supersecretkey'  # Cambia esto en producción

db.init_app(app)
migrate.init_app(app, db)

login_manager = LoginManager(app)
login_manager.login_view = 'login'

from app import routes, models
from app.models import Usuario

@login_manager.user_loader
def load_user(user_id):
    return Usuario.query.get(int(user_id))
