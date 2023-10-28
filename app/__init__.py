from flask import Flask
from config import Config

from flask_login import LoginManager
from app.models import User
from app.database import db
import logging
DB_NAME = 'happydb.db'
login_manager = LoginManager()


def create_app():
    app = Flask(__name__)
    # Load instance-specific configuration
    # app.config.from_pyfile('config.py', silent=True)
    app.config['SECRET_KEY'] = 'secret'
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    app.config['TESTING'] = False
    app.config['LOGIN_DISABLED '] = False
    db.init_app(app)
    # Initialize Flask-Login
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'
    login_manager.login_message_category = 'info'
    login_manager.login_message_category = 'error'
    login_manager.login_message_category = 'success'
    login_manager.login_message_category = 'warning'

    from .models import User
    @login_manager.user_loader
    def load_user(get_id):
        # Replace this with logic to retrieve the user from your database
        return User.query.get(int(get_id))

    
    # Import and register blueprints
    from app.routes.main import main_bp
    from app.routes.auth import auth_bp
    from app.routes.component import component_bp

    app.register_blueprint(main_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(component_bp)
    # Initialize the database with your app
    # Other app setup code can go 
    # with app.app_context():
    #     db.create_all()



    return app


