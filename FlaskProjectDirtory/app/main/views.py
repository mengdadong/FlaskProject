"""
负责视图和路由
"""
import hashlib

from flask import request
from flask import jsonify
from flask import redirect
from flask import session
from flask import render_template

from . import main       #组织路由
from app.models import *
from .forms import TeacherForm
from app import csrf


def setPassword(password):
    password += BaseConfig.SECRET_KEY    #将密码进行新的拼接，就是加盐的加密方式
    md5 = hashlib.md5()
    md5.updata(password.encode())
    return md5.hexdigest()

def loginValid(fun):
    def inner(*args,**kwargs):
        username = request.cookies.get("username")
        id = request.cookies.get("user_id")
        session_username = session.get("username")
        if username == session_username:        #可以在此处添加其他加密方法
            return fun(*args,**kwargs)
        return redirect("/login/")
    return inner

@main.route("/register/",methods=["GET","POST"])
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
    return render_template("register.html",**locals())


@main.route("/login/",methods=["GET","POST"])
def login():
    students = Students.query.all()
    return render_template("students_list.html",**locals())



@main.route("/index/",methods=["GET","POST"])         #后装饰
@loginValid                                           #先装饰
def index():
    students = Students.query.all()
    response = render_template("index.html",**locals())
    #response.set_cokie(")
    return response

@main.route("/logout/",methods=["GET","POST"])
def logout():
    # students = Students.query.all()
    # response = render_template("students_list.html",**locals())
    #response.set_cookie("")
    response = redirect("/login/")
    for key in request.cookies:
        response.delete_cookie(key)
        del session["username"]
    # response.delete_cookie()      #实际上是将值设置为零
    return response

@main.route("/student_list/",methods=["GET","POST"])
def student_list():
    students = Students.query.all()
    response = render_template("students_list.html",**locals())
    return response

@csrf.exempt
@main.route("/add_teacher/",methods=["GET","POST"])
def add_teacher():
    teacher_form = TeacherForm()
    if request.method == "POST":
        name = request.form.get("name")
        age = request.form.get("age")
        gender = request.form.get("gender")
        course = request.form.get("course")

        t = Teachers()
        t.name = name
        t.age = int(age)
        t.gender = int(gender)
        t.course_id = int(course)
        t.save()


    return render_template("add_teacher.html",**locals())
#csrm.exempt 单视图函数避免csrf校验
#csrf.error_headler  重新定义403错误页
@csrf.error_handler
def csrf_token_error(reason):
    print(reason)   #错误信息，The CSRF token is missing.
    return render_template("csrf_403.html",**locals())

@main.route("/csrf_403/")
def csrf_token_error():
    return render_template("csrf_403.html",**locals())

@main.route("/userValid/",methods=["GET","POST"])
def UserValid():
    result = {
        "code":"",
        "data":""
    }
    if request.method == "POST":
        data = request.args.post("username")
        if data:
            user = User.query.filter_by(username = data).first()
            if user:
                result["code"] = 400
                result["data"] = "用户名已经存在"
            else:
                result["code"] = 200
                result["data"] = "用户名未被注册，可以使用"
    else:
        result["code"] = 400
        result["data"] = "请求方式错误"
    return jsonify(result)