from functools import wraps
import jwt
from flask import request, abort
from flask import current_app
import models

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        if "Authorization" in request.headers:
            token = request.headers["Authorization"].split(" ")[1]
        if not token:
            return {
                "message": "Authentication Token is missing!",
                "data": None,
                "error": "Unauthorized"
            }, 401
        try:
            data=jwt.decode(token, current_app.config["SECRET_KEY"], algorithms=["HS256"])
            current_user=models.User.get_by_id(data["id"])
            if current_user is None:
                return {
                "message": "Invalid Authentication token!",
                "data": None,
                "error": "Unauthorized"
            }, 401
        except Exception as e:
            return {
                "message": "Something went wrong",
                "data": None,
                "error": str(e)
            }, 500

        return f(current_user, *args, **kwargs)

    return decorated

def save_general_data(f):
    @wraps(f)
    def decorated(*args,**kwargs):
        try:
            data = {
                "origin" : request.remote_addr,
                "user_agent" : request.user_agent.string,
                "browser" : request.user_agent.browser if request.user_agent.browser else "" ,
                "platform" : request.user_agent.platform if request.user_agent.platform else "" ,
                "version" : request.user_agent.version if request.user_agent.version else "" 
            }
            models.Pc.create(**data)
            return f(*args,**kwargs)
        except Exception as e:
            return {"msg":str(e)}
    return decorated