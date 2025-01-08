import os
from flask import request, jsonify
import jwt
import datetime
from functools import wraps 


def token_required(f):
    @wraps(f)
    def decoder(*args, **kwargs):
        token = request.headers.get('Authorization')
        token = token.split(' ')[1]
        if not token:
            return jsonify({'message': 'Token is missing'}), 401
        try:
            data = jwt.decode(token, os.getenv('SECRET_KEY'), algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            return jsonify({'message': 'Token is expired'}), 401
        except jwt.InvalidTokenError:
            return jsonify({'message': 'Token is invalid'}), 401
        return f(data,*args, **kwargs)
    return decoder


def generate_token(userid): 
    payload = {
        'userid': userid,
        'exp': datetime.datetime.utcnow() + datetime.timedelta(days=7)
    } 
    token = jwt.encode(payload, os.getenv('SECRET_KEY'), algorithm='HS256')
    return token