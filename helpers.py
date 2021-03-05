from flask import session, abort
from functools import wraps


def authorize(f):
    @wraps(f)
    def decorated_function(*args, **kws):
        if session.get("username") is None:
            return abort(401)

        return f(*args, **kws)
    return decorated_function
