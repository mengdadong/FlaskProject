"""
负责视图和路由
"""
import hashlib

from flask import request
from flask import render_template
from FlaskDirtory.main import app
from FlaskDirtory.models import *


def setPassword(password):
    md5 = hashlib.md5()
    md5.update(password.encode())
    return md5.hexdigest()

@app.route("/register/",methods=["GET","POST"])
def register():
    if request.method == "POST":
        form_data = request.form
        username = form_data.get("username")
        password = form_data.get("password")
        identity = form_data.get("identity")
        user = User()
        user.username = username
        user.password = setPassword(password)
        user.identity = int(identity)
        user.save()
    students = Students.query.all()
    return render_template("register.html", **locals())


@app.route("/login/",methods=["GET","POST"])
def login():
    students = Students.query.all()
    response = render_template("students_list.html", **locals())
    #response.set_cookie("")
    return response



@app.route("/index/",methods=["GET","POST"])
def index():
    students = Students.query.all()
    response = render_template("students_list.html", **locals())
    #response.set_cookie("")
    return response

@app.route("/logout/",methods=["GET","POST"])
def logout():
    students = Students.query.all()
    response = render_template("students_list.html", **locals())
    #response.set_cookie("")
    return response


@app.route("/student_list/",methods=["GET","POST"])
def student_list():
    students = Students.query.all()
    response = render_template("students_list.html", **locals())
    #response.set_cookie("")
    return response

