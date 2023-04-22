from re import A
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager

db = SQLAlchemy()
DB_NAME = "database.db"

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'the is a secret key for my app'
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'

    db.init_app(app)

    from .views import views
    from .auth import auth
    
    # registering the blueprints
    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')

    from .models import User, Note
    # we write this so that the model file runs
    # and creates our database

    with app.app_context():
        db.create_all()

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    # now we tell flask how to load a user
    # how as in, how to fetch data from the db
    # in this case it is the primary key
    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))

    return app

# this method checks if the database exists
# because if it exists,  we dont want to create
# it again as that will overwrite it
def create_datbase(app):
    if not path.exists('website/' + DB_NAME):
        db.create_all(app=app)
        print('Created Database!')