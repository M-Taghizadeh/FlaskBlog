from . import admin ### . means __init__.py
from flask import session, render_template, request, abort, flash ### abort for errors
from mod_users.froms import LoginForm
from mod_users.models import User

# important ... 
# session is a dict -----> for using session you should set a 'secret key' for your web app
# client side : Cookie,    server side : Session

@admin.route("/")
def index():
    return "Hello from admin index.."


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

        session['email'] = user.email
        session['user_id'] = user.id

        print(session)
        return "Loged in Successfuly"
        
    if session.get('email') is not None:
        return "you are already Loged in.."

    return render_template("admin/login.html", form=form)