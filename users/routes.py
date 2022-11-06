from flask import render_template, url_for, flash, redirect, Blueprint
from flask_login import login_user, current_user, logout_user, login_required, login_manager
from models.user import User
from models.post import Post
from flask_bcrypt import bcrypt
from db import db
from flask import current_app as app
from users.forms import (RegistrationForm, LoginForm)

users = Blueprint('users', __name__)


@users.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
      return redirect(url_for('homepage'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created! You can log in now', 'success')
        return redirect(url_for('users.login'))
    return render_template('register.html', title='Register', form=form, user = current_user)


@users.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('homepage'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user)
            redirect(url_for('homepage'))
        else:
            flash('Error. Please check that you have provided the right details', 'danger')
    return render_template('login.html', title='Login', form=form, user = current_user)


@users.route("/user/<string:username>")
def user_posts(username):
    user = User.query.filter_by(username=username).first_or_404()
    posts = Post.query.filter_by(author=user)\
        .order_by(Post.date_posted.desc())
    return render_template('user_posts.html', posts=posts, user=user)



@users.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('homepage'))


'''@app.login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))'''