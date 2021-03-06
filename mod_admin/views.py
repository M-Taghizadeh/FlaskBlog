from . import admin ### . means __init__.py
from flask import session, render_template, request, abort, flash ### abort for errors
from mod_users.froms import LoginForm, RegisterForm
from mod_users.models import User
from .utils import admin_only_view ### my decorator
from flask import redirect, url_for
from mod_blog.forms import PostForm, CategoryForm
from mod_blog.models import Post, Category
from app import db
from sqlalchemy.exc import IntegrityError
from mod_uploads.forms import FileUploadForm
from mod_uploads.models import File
from werkzeug.utils import secure_filename
import uuid # return a hash

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

@admin.route("/posts/new", methods=["GET", "POST"])
@admin_only_view
def create_post():
    form = PostForm(request.form)

    categories = Category.query.order_by(Category.id).all()
    form.categories.choices = [(category.id, category.name) for category in categories]
    
    if request.method == "POST":
        if not form.validate_on_submit():
            return "form is not valid."

        new_post = Post()
        new_post.title = form.title.data
        new_post.summary = form.summary.data
        new_post.content = form.content.data
        new_post.slug = form.slug.data
        # point 
        new_post.categories = [Category.query.get(category_id) for category_id in form.categories.data]

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
            flash("Slug Duplicated.")
            print(IntegrityError)

    return render_template("admin/create_post.html", form=form)

@admin.route("/users/", methods=["GET"])
@admin_only_view
def list_users():
    users = User.query.order_by(User.id.desc()).all() ### select * from users
    return render_template("admin/list_users.html", users = users)

@admin.route("users/new", methods=["GET"])
@admin_only_view
def get_create_user():
    form = RegisterForm() # we not use fill RegisterForm because methods=["GET"]
    return render_template("admin/create_user.html", form=form)

@admin.route("users/new", methods=["POST"])
@admin_only_view
def post_create_user():
    form = RegisterForm(request.form) # we not use fill RegisterForm because methods=["GET"]
    
    if not form.validate_on_submit():
        return render_template("admin/create_user.html", form = form)
        
    if not form.password.data == form.confirm_password.data:
        error_msg = "Password and Confirm Password dose not match!!!"
        form.password.errors.append(error_msg)
        form.confirm_password.errors.append(error_msg)
        return render_template("admin/create_user.html", form = form)

    ### Method 1 for handeling user duplicated:
    old_user = User.query.filter(User.email.ilike(form.email.data)).first()
    if old_user:
        flash("Email in use.", category="error")
        return render_template("admin/create_user.html", form = form)

    
    new_user = User()
    new_user.full_name = form.full_name.data
    new_user.email = form.email.data
    new_user.set_pass(form.password.data)
    db.session.add(new_user)
    db.session.commit()
    flash("Your Welcome dear " + form.full_name.data, category="tertiary")
        
    return render_template("admin/create_user.html", form=form)

@admin.route("/posts/", methods=["GET"])
@admin_only_view
def list_posts():
    posts = Post().query.order_by(Post.id.desc()).all()
    return render_template("admin/list_posts.html", posts=posts)

@admin.route("/posts/delete/<int:post_id>", methods=["GET"])
@admin_only_view
def delete_post(post_id):
    post = Post().query.get_or_404(post_id)
    db.session.delete(post)
    db.session.commit()
    flash("Post Deleted!!!")
    return redirect(url_for("admin.list_posts"))

### this form fill with old value of post form from post method from database
@admin.route("posts/modify/<int:post_id>", methods=["GET", "POST"])
@admin_only_view
def modify_post(post_id):
    post = Post().query.get_or_404(post_id)
    form  = PostForm(obj=post)

    categories = Category.query.order_by(Category.id).all()
    ### set choices in view
    form.categories.choices = [(category.id, category.name) for category in categories]

    ### challenge :
    if request.method != 'POST':
        form.categories.data = [category.id for category in post.categories]

    if request.method == "POST":
        if not form.validate_on_submit():
            return render_template("admin/modify_post.html", form=form, post=post)
        post.title = form.title.data
        post.summary = form.summary.data
        post.content = form.content.data
        post.slug = form.slug.data
        post.categories = [Category.query.get(category_id) for category_id in form.categories.data]

        try:
            db.session.commit()
            flash("Post modified.")
        except IntegrityError:
            db.session.rollback()
            flash("Slug Duplicated.")
        
    return render_template("admin/modify_post.html", form=form, post=post)











@admin.route("/categories/new", methods=["GET", "POST"])
@admin_only_view
def create_category():
    form = CategoryForm(request.form)
    if request.method == "POST":
        if not form.validate_on_submit():
            return "form is not valid."
        new_category = Category()
        new_category.name = form.name.data
        new_category.description = form.description.data
        new_category.slug = form.slug.data

        try:
            db.session.add(new_category)
            db.session.commit()
            flash("Category Created :)")
            return redirect(url_for("admin.index"))
        except IntegrityError:
            db.session.rollback()
            flash("Slug Duplicated.")
            print(IntegrityError)

    return render_template("admin/create_category.html", form=form)


@admin.route("/categories/", methods=["GET"])
@admin_only_view
def list_categories():
    categories = Category().query.order_by(Category.id.desc()).all()
    return render_template("admin/list_categories.html", categories=categories)

@admin.route("/categories/delete/<int:category_id>", methods=["GET"])
@admin_only_view
def delete_category(category_id):
    category = Category().query.get_or_404(category_id)
    db.session.delete(category)
    db.session.commit()
    flash("Category Deleted!!!")
    return redirect(url_for("admin.list_categories"))

@admin.route("categories/modify/<int:category_id>", methods=["GET", "POST"])
@admin_only_view
def modify_category(category_id):
    category = Category().query.get_or_404(category_id)
    form  = CategoryForm(obj=category)

    if request.method == "POST":
        if not form.validate_on_submit():
            return render_template("admin/modify_category.html", form=form, category=category)
        category.name = form.name.data
        category.description = form.description.data
        category.slug = form.slug.data
        try:
            db.session.commit()
            flash("Category modified.")
        except IntegrityError:
            db.session.rollback()
            flash("Slug Duplicated.")
        
    return render_template("admin/modify_category.html", form=form, category=category)



### UPLOAD:
@admin.route("/library/upload", methods=["GET", "POST"])
@admin_only_view
def upload_file():
    form = FileUploadForm() ### default --> fill with : form.data

    if request.method == "POST":
        # print(request.form)
        # print(request.files)
        # print(form.data) ### contain request.form and request.files
        if not form.validate_on_submit:
            return "Not Valid!"
        
        # save file in static/uploads
        print(dir(form.file.data)) ### dir for showing all attr of an object thats very important

        # create a random hash name
        filename = f'{uuid.uuid1()}_{secure_filename(form.file.data.filename)}' # secure_filename ---> exp file name : ../filename (bug in unix base os)
        new_file = File()
        new_file.filename = filename
        db.session.add(new_file)
        db.session.commit()
        form.file.data.save(f'static/uploads/{filename}')
        flash(f'File Uploaded on { url_for("static", filename="uploads/"+filename, _external=True) }')
    return render_template("admin/upload_file.html", form=form)