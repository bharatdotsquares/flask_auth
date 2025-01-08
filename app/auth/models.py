import os
from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import jwt
from app.utils.token import generate_token
db = SQLAlchemy()

project_dir = os.path.dirname(os.path.abspath(__file__))
# print(os.path.join(project_dir,"app" ,"db","database.db"))
def connect_db(app):
    app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL")
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = os.getenv("TRACK_MODIFICATIONS")
    db.app = app
    db.init_app(app)
    migrate = Migrate(app,db)
    with app.app_context():
        db.create_all()


class User(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    username = db.Column(db.String,unique=True,nullable=False)
    email = db.Column(db.String(255),unique=True,nullable=False)
    password = db.Column(db.String(255),nullable=False)
    is_active = db.Column(db.Boolean, default=True)
    profile_pic = db.Column(db.String(255),nullable=True,default="https://www.gravatar.com/avatar/2c7d99fe281ecd3bcd65ab915bac6dd5?s=250")

    
    def __repr__(self):
        return f"User('{self.username}', '{self.email}')"
    
    def __init__(self, username=None, email=None, password=None,filename=None):
        self.username = username
        self.email = email
        self.password = self.set_password(password)
        self.profile_pic = filename
        self.is_active = True
        
        
    def set_password(self, password):
        self.password = generate_password_hash(password)
        return self.password
    
    def check_password(self, password):
        return check_password_hash(self.password, password)
    
    
    def toJSON(self):
        return {"id": self.id, "username": self.username, "email": self.email, "is_active": self.is_active, "profile_pic": self.profile_pic}
    
    
    def generate_token(self):
        print(self)
        return generate_token(self.id)
    
    @staticmethod
    def authenticate(username,password):
        user = User.query.filter_by(username=username).first()
        if user and user.check_password(password):
            return user
        return None
    
    @staticmethod
    def isExist(username=None, email=None):
        if username:
            user = User.query.filter_by(username=username).first()
            if user:
                return True
        if email:
            user = User.query.filter_by(email=email).first()
            if user:
                return True
        return False
    @staticmethod
    def getAll():
        users = User.query.all()
        results = []
        for user in users:
            results.append(user.toJSON())
        return results
    
    @staticmethod
    def getById(id):
        user = User.query.get(id)
        if user:
            return user.toJSON()
        return None
    