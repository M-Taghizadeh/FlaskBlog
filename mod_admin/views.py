from . import admin ### . means __init__.py
from flask import session, render_template, request, abort, flash ### abort for errors
from mod_users.froms import LoginForm
from mod_users.models import User
from .utils import admin_only_view ### my decorator
from flask import redirect, url_for
from mod_blog.forms import CreatePostForm
from mod_blog.models import Post
from app import db
from sqlalchemy.exc import IntegrityError

# important ... 
# session is a dict -----> for using session you should set a 'secret key' for your web app
# client side : Cookie,    server side : Session

@admin.route("/")
@admin_only_view
def index():
    # Method 1 :
    # if session.get("user_id") is None:
    #     abort(401) ### Unauthorized
    # Method 2 : Decorator utils

    return render_template("admin/index.html")


@admin.route("/login/", methods=["GET", "POST"])
def login():
    # session["name"] = "mohammad"
    # print(session)
    # session.clear()
    # print(session.get('name'))
    form = LoginForm(request.form)
    if request.method == 'POST':
        if not form.validate_on_submit():
            abort(400)

        user = User.query.filter(User.email.ilike(f'{form.email.data}')).first() # Incase Sensetive Like () ---> ilike() in sql alchemy
        if not user:
            # return "Incorrect Credentials!!!", 400 ### status code 400 rather than 200
            
            ### (flash message save in session)     
            flash("Incorrect Credentials!!!", category="error") ### you must set flash message in view 
            print(session)
            return render_template("admin/login.html", form=form)
        if not user.check_pass(form.password.data):
            flash("Incorrect Password", category="error")
            print(session)
            return render_template("admin/login.html", form=form)
        if not user.is_admin():
            flash("Incorrect Credentials!!!", category="error")
            print(session)
            return render_template("admin/login.html", form=form)

        session['email'] = user.email
        session['user_id'] = user.id
        session['role'] = user.role

        print(session)
        return redirect(url_for("admin.index"))
        
    if session.get('role') is not None:
        return redirect(url_for("admin.index"))

    return render_template("admin/login.html", form=form)

@admin.route("/logout/", methods=["GET"])
@admin_only_view
def logout():
    session.clear()
    flash("You logged out successfuly.", category="warning")

    return redirect(url_for('admin.login'))

@admin.route("posts/new", methods=["GET", "POST"])
@admin_only_view
def create_post():
    form = CreatePostForm(request.form)
    if request.method == "POST":
        if not form.validate_on_submit():
            return "form is not valid."
        new_post = Post()
        new_post.title = form.title.data
        new_post.summary = form.summary.data
        new_post.content = form.content.data
        new_post.slug = form.slug.data

        try:
            db.session.add(new_post)
            print(new_post.title)
            print(new_post.summary)
            print(new_post.content)
            print(new_post.slug) 
            db.session.commit()
            flash("Post Created :)")
            return redirect(url_for("admin.index"))
        except IntegrityError:
            db.session.rollback()
            print(IntegrityError)

    return render_template("admin/create_post.html", form=form)