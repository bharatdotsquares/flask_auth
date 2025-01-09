import os
from flask import request,jsonify,render_template
from app import app
from app.auth.models import User,db
from app.utils.const import HttpStatus
from app.utils.res import res


 
def home():
    return render_template('instructions.html')


def login():
    try:
        username = request.form.get('username')
        password = request.form.get('password')
        
        isExist = User.isExist(username)
        if not isExist:
            return res(False, "Username not exist.", None,HttpStatus.BAD_REQUEST)
        
        user = User.authenticate(username,password)
        if not user:
            return res(False, "Invalid username or password.", None,HttpStatus.BAD_REQUEST)

        token = user.generate_token()
        return res(True,"User Loggedin successfully",{"token": token,"user":user.toJSON()},HttpStatus.OK)
        
    except Exception as error:
        return res(False,"server error", None,HttpStatus.SERVER_ERROR)
 
def register():
    try:
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        file = request.files.get('profile_pic')     
         
        isExist = User.isExist(username=username, email=email)
        if isExist:
            return res(False, "Username or email already exists.", None,HttpStatus.BAD_REQUEST)
        if file:
            file.save(app.config['STATIC_FOLDER'] + file.filename)
        new_upload = User(username=username,email=email,password=password, filename=file.filename)
        db.session.add(new_upload)
        db.session.commit()
        return res(True,"User Loggedin successfully",new_upload.toJSON(),HttpStatus.OK) 
    except Exception as error:
        db.session.rollback()
        print(error)
        return res(False,"server error", None,HttpStatus.SERVER_ERROR)


def user(data):
    try:
        user = User.getById(id=data.get('userid'))
        return  res(True,"User Loggedin successfully",user,HttpStatus.OK)
    except Exception as error:
        return res(False,"server error", None,HttpStatus.SERVER_ERROR)
    
def users(data):
    try:
        curruser = User.getById(id=data.get('userid'))
        users = User.getAll()
        payload = {"curruser":curruser,"users":users}
        return res(True,"User retrival successfully",payload,HttpStatus.OK)
    except Exception as error:
        print(error)
        return res(False,"server error", None,HttpStatus.SERVER_ERROR)