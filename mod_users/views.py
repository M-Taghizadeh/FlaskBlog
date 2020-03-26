# import user blueprint 
# . : __init__.py
from . import users
from .froms import RegisterForm
from flask import request, render_template, flash
from .models import User
from app import db

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

        new_user = User()
        new_user.full_name = form.full_name.data
        new_user.email = form.email.data
        new_user.set_pass(form.password.data)
        db.session.add(new_user)
        db.session.commit()
        flash("Your Welcome dear " + form.full_name.data, category="tertiary")

    return render_template("users/register.html", form = form)