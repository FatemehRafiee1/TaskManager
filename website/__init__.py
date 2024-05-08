from flask import Flask 
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from sqlalchemy import create_engine
from sqlalchemy_utils import create_database, database_exists

from .tools import SQL_PASS

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)

    username = 'root'
    host = 'localhost'
    port = 3306
    DB_NAME = 'testdb'

    url = f"mysql://{username}:{SQL_PASS}@{host}:{port}/{DB_NAME}"
    if not database_exists(url):
        create_database(url)

    app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql://{username}:{SQL_PASS}@{host}/{DB_NAME}'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.secret_key = 'your_secret_key'
    
    db.init_app(app)
    
    # Initialize Flask-Login's LoginManager
    login_manager = LoginManager(app)
    # login_manager.login_view =  'auth.login'
    # login_manager = LoginManager()
    # login_manager.init_app(app)

    from .models import User
    
    from .home import task_manager
    from .auth import auth
    
    app.register_blueprint(task_manager, url_prefix='/') 
    app.register_blueprint(auth, url_prefix='/') 
    
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    with app.app_context():
        db.create_all()
    
    return app