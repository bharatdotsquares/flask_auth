import os
from flask import Flask
from dotenv import load_dotenv

load_dotenv()

# from flask_wtf import CSRFProtect
from flask_cors import CORS
from app.auth.models import connect_db 
app = Flask(__name__)

project_dir = os.path.dirname(os.path.abspath(__file__))
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
app.config['STATIC_FOLDER'] = project_dir + '\\static\\'
# CSRF = CSRFProtect(app)
CORS(app)
connect_db(app)

from app.auth.routes import *