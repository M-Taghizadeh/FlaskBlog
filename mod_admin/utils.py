### check user loged in or not

from flask import session, abort

# if session.get("user_id") is None:

def admin_only_view(func):
    def decorator(*args, **kwargs):
        if session.get("user_id") is None: # for Unauthorized..
            abort(401)
        if session.get("role") is None:    # for Unaccess..
            abort(403)
        return func(*args, **kwargs)
    return decorator