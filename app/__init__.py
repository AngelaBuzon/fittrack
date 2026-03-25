from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_bcrypt import Bcrypt
from config import Config

db = SQLAlchemy()
login_manager = LoginManager()
bcrypt = Bcrypt()
login_manager.login_view = 'auth.login'

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    login_manager.init_app(app)
    bcrypt.init_app(app)

    from app.blueprints.auth import auth_bp
    from app.blueprints.musculacion import musculacion_bp
    from app.blueprints.rutas import rutas_bp
    from app.blueprints.dashboard import dashboard_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(musculacion_bp, url_prefix='/musculacion')
    app.register_blueprint(rutas_bp, url_prefix='/rutas')
    app.register_blueprint(dashboard_bp, url_prefix='/dashboard')

    return app