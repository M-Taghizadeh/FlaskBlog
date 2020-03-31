from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from Config import Development
from redis import Redis
from flask_mail import Mail

app = Flask(__name__)
app.config.from_object(Development)
db = SQLAlchemy(app)
migrate = Migrate(app, db)
redis = Redis.from_url(app.config['REDIS_SERVER_URL'])
mail = Mail(app)

# import view
from views import index
# import blueprints
from mod_admin import admin
from mod_users import users
from mod_blog import blog
from mod_uploads import uploads

# register blueprints
app.register_blueprint(admin)
app.register_blueprint(users)
app.register_blueprint(blog)
app.register_blueprint(uploads)