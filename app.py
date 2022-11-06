from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os
from flask_login import LoginManager, UserMixin, current_user
from flask_bcrypt import Bcrypt
from db import db
from models.user import User

# I came to define this outside the create app function given the error
#login_manager = LoginManager(app)

def create_app():
    base_dir = os.path.dirname(os.path.realpath(__file__))

    app = Flask(__name__)

    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + \
            os.path.join(base_dir, 'blog.db')
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config['SECRET_KEY'] = '862b3bfe6e2fc3acdcc334638cfca828878b6b82'
    db.init_app(app)

   
    bcrypt = Bcrypt(app)
    bcrypt.init_app(app)

    login_manager = LoginManager()
    login_manager.login_view = 'users.login'
    login_manager.login_message_category = 'info'
    #login_manager.init_app(app)


    @app.before_first_request
    def create_tables():
        db.create_all()

    from users.routes import users
    from posts.routes import posts
    from main.routes import main
    app.register_blueprint(users)
    app.register_blueprint(posts)
    app.register_blueprint(main)

    return app

 


