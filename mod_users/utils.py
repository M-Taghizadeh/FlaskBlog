import random
from app import redis
from app import mail
from flask import url_for # for create full url for activate registeration.

# Redis => [Key Value DataBse] your data have a key for example => 6_register : 12345 [6 is user id mode is register and token is 12345]
def add_to_redis(user, mode):
    token = random.randint(10000, 99999)
    name = f'{user.id}_{mode.lower()}'

    # add redis => name, value, expiry_time(s)
    redis.set(name, token, 14400)

    return token

def send_signup_email(user, token):
    url = url_for("users.confirm_registeration", email = user.email, token = token, _external=True)

    sender ='taghizadeh.py@gmail.com'
    recipients = [user.email] 
    subject = "Flask Blog Registeration Confirm"
    body = f'Hello dear {user.full_name}<br>Here is your token : {url}<br><br>this token expire in 4 houre.'
    mail.send_message(sender=sender, recipients=recipients, subject=subject, html=body)

def get_from_redis(user, mode):
    name = f'{user.id}_{mode.lower()}'
    return redis.get(name=name) # get a byte string we must cast to str

def delete_from_redis(user, mode):
    name = f'{user.id}_{mode.lower()}'
    redis.delete(name)
