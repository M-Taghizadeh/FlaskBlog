from . import blog
from flask import render_template, abort, request
from .models import Post, Category
from app import db
from flask_sqlalchemy import get_debug_queries ### for see what query send to or db
from sqlalchemy import or_ ### by default is and
from .forms import SearchForm

@blog.route("/")
def index():
    # Search Form
    search_form = SearchForm()

    # in the past we use all() methos for showing post :(
    # but we can paginate post , see it bellow :)
    # List of Posts 
    # posts = Post.query.all()

    # pagination
    page = request.args.get("p", default=1, type=int) 
    posts = Post.query.paginate(page, 5)

    return render_template("blog/index.html", posts=posts, search_form=search_form)

@blog.route("/<string:slug>")
def single_post(slug):

    # Search Form   
    search_form = SearchForm()

    post = Post.query.filter(Post.slug == slug).first_or_404()
    # if not post:
    #     abort(404)

    # in top we have 2 method for handel if page not found : 1:first_or_404() or 2:abort(404)
    return render_template("blog/single_post.html", post=post, search_form=search_form)

@blog.route("/search/")
def search_blog():
    # Search Form   
    search_form = SearchForm()

    """ query string : domain.com/blog/search/?q=hello """
    search_query = request.args.get('search_query', '') # default is None we override that to ''
    
    title_cnd = Post.title.ilike(f'%{search_query}%')
    summary_cnd = Post.summary.ilike(f'%{search_query}%')
    content_cnd = Post.content.ilike(f'%{search_query}%')

    ### using or_ SQLAlchemy : by default is and
    found_posts = Post.query.filter(or_(
        title_cnd,
        summary_cnd,
        content_cnd
    )).all()

    print(found_posts)
    print(get_debug_queries()) ### show queries that was sent to database
    return render_template("blog/search.html", posts=found_posts, search_form=search_form, search_query=search_query)

@blog.route("/category/<string:slug>")
def single_category(slug):
    # Search Form   
    search_form = SearchForm()

    category = Category.query.filter(Category.slug == slug).first_or_404()
    return render_template("blog/single_category.html", posts=category.posts, search_form=search_form, category_name = category.name)
