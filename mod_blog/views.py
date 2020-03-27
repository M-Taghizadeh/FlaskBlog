from . import blog
from flask import render_template
from .models import Post
from app import db

@blog.route("/")
def index():

    # List of Posts
    posts = Post.query.all()
    return render_template("blog/index.html", posts=posts)

@blog.route("/<string:slug>")
def single_post(slug):
    post = Post.query.filter(Post.slug == slug).first()

    return post.title