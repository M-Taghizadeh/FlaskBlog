### check user loged in or not

from flask import session, abort
from functools import wraps ### baraye ejade name haye motefavet baraye decorator e 'admin_only_view'
# if session.get("user_id") is None:

def admin_only_view(func):
    @wraps(func) ### name e decorator ro func set mikoneh.. :)
    def decorator(*args, **kwargs):
        if session.get("user_id") is None: # for Unauthorized..
            abort(401)
        if session.get("role") is None:    # for Unaccess..
            abort(403)
        return func(*args, **kwargs)
    return decorator