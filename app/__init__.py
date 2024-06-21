# __init__.py

from flask import Flask
import secrets
from flask_pymongo import PyMongo
from flask_cors import CORS
from dotenv import load_dotenv
import os
from flask_mail import Mail
import boto3, s3fs
#access your MongoDB Atlas Cluster
load_dotenv()

connection_string : str = os.environ.get("CONNECTION_STRING")
mail_password : str = os.environ.get("MAIL_PASSWORD")
access_id: str = os.environ.get("aws_access_key_id")   
access_key: str = os.environ.get("aws_secret_access_key") 

app = Flask(__name__)
app.config["MONGO_URI"] = connection_string
mongo = PyMongo(app)
cors = CORS(app)
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = "shubham.srivastava@vedsu.com"
app.config['MAIL_PASSWORD'] = "ibwd xcqh uvgb uavn"
app.config["MAIL_USE_TLS"] = False
app.config["MAIL_USE_SSL"] = True
mail = Mail(app)

s3_resource = boto3.resource(
    service_name = "s3",
    region_name = 'us-east-1',
    aws_access_key_id = access_id,
    aws_secret_access_key = access_key

)
s3_client = boto3.client(
    service_name = "s3",
    region_name = 'us-east-1',
    aws_access_key_id = access_id,
    aws_secret_access_key = access_key)
app.secret_key = secrets.token_hex(16)
from app import routes