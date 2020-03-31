# import user blueprint 
# . : __init__.py
from . import users
from .froms import RegisterForm
from flask import request, render_template, flash
from .models import User
from app import db
from sqlalchemy.exc import IntegrityError
from .utils import add_to_redis, send_signup_email, get_from_redis, delete_from_redis

@users.route("/register/", methods=["GET", "POST"])
def register():
    form = RegisterForm(request.form)
    if request.method == "POST":
        if not form.validate_on_submit():
            return render_template("users/register.html", form = form)
        
        if not form.password.data == form.confirm_password.data:
            error_msg = "Password and Confirm Password dose not match!!!"
            form.password.errors.append(error_msg)
            form.confirm_password.errors.append(error_msg)
            return render_template("users/register.html", form = form)

        ### Method 1 for handeling user duplicated:
        old_user = User.query.filter(User.email.ilike(form.email.data)).first()
        if old_user:
            flash("Email in use.", category="error")
            return render_template("users/register.html", form = form)

        new_user = User()
        new_user.full_name = form.full_name.data
        new_user.email = form.email.data
        new_user.set_pass(form.password.data)
        db.session.add(new_user)
        db.session.commit()

        # send verification email:
        token = add_to_redis(new_user, "register")
        send_signup_email(new_user, token)

        flash("Your Welcome dear " + form.full_name.data, category="tertiary")
        
        ### Method 2 for handeling user duplicated:
        # try:
        #     db.session.add(new_user)
        #     db.session.commit()
        #     flash("Your Welcome dear " + form.full_name.data, category="tertiary")
        # except IntegrityError:
        #     db.session.rollback()
        #     flash("Email in use.", category="error")


    return render_template("users/register.html", form = form)

@users.route('/confirm/')
def confirm_registeration():
    email = request.args.get("email")
    token = request.args.get("token")

    user = User.query.filter(User.email.ilike(email)).first()
    if not user:
        return "User not found!"
    
    token_from_redis = get_from_redis(user, "register") # get a byte string we must cast to str
                                                        # cat with decode("utf-8")
    if not token_from_redis:
        return "Wrong/Expired Token."
    
    if token != token_from_redis.decode("UTF-8"):
        return "Wrong or Expired Token."

    ### activate user and delete token from redis
    delete_from_redis(user, "register")
    user.active = True
    db.session.commit()

    return "Your account activated."