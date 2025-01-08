from app import app
from app.auth.controller import home, login,register,user,users
from app.utils.token import token_required
@app.route('/')
def home_route():
    return home()

@app.route('/login',methods=['POST'])
def login_route():
    return login()

@app.route('/register',methods=['POST'])
def register_route():
    return register()

@app.route('/user',methods=['GET'])
@token_required #wrap function by functools for authenticating token
def user_route(data):
    return user(data)
@app.route('/users',methods=['GET'])
@token_required #wrap function by functools for authenticating token
def users_route(data):
    return users(data)