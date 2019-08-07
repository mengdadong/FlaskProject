import os

import pymysql
from flask import Flask

from flask_sqlalchemy import SQLAlchemy

pymysql.install_as_MySQLdb()

app = Flask(__name__)

app.config.from_object('config.DebugConfig')

models = SQLAlchemy(app) #关联sqlalchemy和flask应用





# BASE_DIR = os.path.abspath(os.path.dirname(__file__))

# app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///"+os.path.join(BASE_DIR,"Student.sqlite")
# app.config["SQLALCHEMY_COMMIT_ON_TEARDOWN"] = True
# app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True

#app.config.from_pyfile("settings.py")
