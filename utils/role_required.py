from flask_jwt_extended import get_jwt
from functools import wraps
from flask import make_response

def role_required(allowed_role):
    def wrapper(fn):
        @wraps(fn)
        def decorator(*args,**kwargs):
            claims = get_jwt()
            role = claims.get("role")
            if role not in allowed_role:
                return make_response({"message":"Forbidden"},403)
            return fn(*args,**kwargs)
        return decorator
    return wrapper