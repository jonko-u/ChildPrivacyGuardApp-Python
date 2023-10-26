from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy

from flask_login import LoginManager
from app.models import User
db = SQLAlchemy()
DB_NAME = 'happydb.db'
def create_app():
    app = Flask(__name__)
    # Load instance-specific configuration
    # app.config.from_pyfile('config.py', silent=True)
    app.config['SECRET_KEY'] = 'secret'
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    db.init_app(app)
    # Import and register blueprints
    from app.routes.main import main_bp
    from app.routes.auth import auth_bp

    app.register_blueprint(main_bp)
    app.register_blueprint(auth_bp)
    # Initialize the database with your app
    # Other app setup code can go 
    with app.app_context():
        db.create_all()



    return app