from types import DynamicClassAttribute
from flask_login import LoginManager, UserMixin
from db import db
from flask_login import login_manager

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(30), nullable = False)
    username = db.Column(db.String(20), unique = True, nullable = False)
    email = db.Column(db.String(120), unique = True, nullable = False)
    password = db.Column(db.String(20), nullable = False)
    user_id = db.Column(db.Integer, db.ForeignKey('user_id'), nullable = False)
    #user_posts = db.relationship('Post', back_populates = 'created_by', lazy = True)
  
    def __repr__(self):
        return f"User('{self.username}', '{self.email}')"