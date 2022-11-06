from flask import render_template, request, Blueprint
from models.post import Post


main = Blueprint('main', __name__)



@main.route("/")
def homepage():
    posts = Post.query.order_by(Post.date_posted.desc())
    context = {
        "posts": posts
    }
    return render_template('homepage.html', **context)


@main.route("/about")
def about():
    return render_template('about.html', title='About')