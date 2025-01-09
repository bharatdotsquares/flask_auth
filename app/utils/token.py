import os
from flask import request, jsonify
import jwt
import datetime
from functools import wraps 
from app.utils.res import res
from app.utils.const import HttpStatus
def token_required(f):
    @wraps(f)
    def decoder(*args, **kwargs):
        token = request.headers.get('Authorization')
        if not token:
            return res(False, 'Token is missing', None,HttpStatus.BAD_REQUEST)
        try:
            token = token.split(' ')[1]
            data = jwt.decode(token, os.getenv('SECRET_KEY'), algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            return res(False, 'Token is expired', None,HttpStatus.BAD_REQUEST)
        except jwt.InvalidTokenError:
            return res(False, 'Token is invalid', None,HttpStatus.BAD_REQUEST)
        except:
            return res(False, 'Token is missing', None,HttpStatus.BAD_REQUEST)
        return f(data,*args, **kwargs)
    return decoder


def generate_token(userid): 
    payload = {
        'userid': userid,
        'exp': datetime.datetime.utcnow() + datetime.timedelta(days=7)
    } 
    token = jwt.encode(payload, os.getenv('SECRET_KEY'), algorithm='HS256')
    return token