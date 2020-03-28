from . import blog
from flask import render_template, abort
from .models import Post
from app import db

@blog.route("/")
def index():

    # List of Posts
    posts = Post.query.all()
    return render_template("blog/index.html", posts=posts)

@blog.route("/<string:slug>")
def single_post(slug):
    post = Post.query.filter(Post.slug == slug).first_or_404()
    # if not post:
    #     abort(404)

    # in top we have 2 method for handel if page not found : 1:first_or_404() or 2:abort(404)
    return render_template("blog/single_post.html", post=post)