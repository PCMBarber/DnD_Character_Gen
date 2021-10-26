from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from numpy import genfromtxt
from os import getenv
from aws_xray_sdk.core import xray_recorder
from aws_xray_sdk.ext.flask.middleware import XRayMiddleware

def Load_Data(file_name):
    data = genfromtxt(file_name, delimiter=',', skip_header=0, converters={0: lambda s: str(s)})
    return data.tolist()

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = ("mysql+pymysql://" + getenv('MYSQL_USER') + ":" + getenv('MYSQL_PWD') + "@" + getenv('MYSQL_IP') + "/" + getenv('MYSQL_DB'))
app.config['SECRET_KEY'] = getenv('MYSQL_SK')

db = SQLAlchemy(app)

login_manager = LoginManager(app)
login_manager.login_view = 'login'

xray_recorder.configure(service='My application')
XRayMiddleware(app, xray_recorder)

from application import models

db.create_all()

try:
    file_name = "../feats.csv"
    data = Load_Data(file_name) 
    for i in data:
        record = feat(**{
            'id' : i[0],
            'name' : i[1],
            'effects' : i[2],
            'skillmodify' : i[3]
        })
        db.session.add(record)
        db.session.commit()
except:
    db.session.rollback()

from application import routes
