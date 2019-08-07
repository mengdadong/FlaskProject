import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
print(BASE_DIR)

#app.config返回类字典对象，里面用来存放当前app实例的配置

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///"+os.path.join(BASE_DIR,"Demo.sqlite")
app.config["SQLALCHEMY_COMMIT_ON_TEARDOWN"] = True
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True

models = SQLAlchemy(app) #关联sqlalchemy和flask应用

class BedRoom(models.Model):
    __tablename__ = "bedroom" #表名
    id = models.Column(models.Integer,primary_key = True) #字段
    name = models.Column(models.String(32),unique = True)


class Student(models.Model):
    __tablename__ = "students" #表名
    id = models.Column(models.Integer,primary_key = True) #字段
    name = models.Column(models.String(32),unique = True)

    room_id = models.Column(models.Integer,models.ForeignKey('bedroom.id'))

class Course(models.Model):
    __tablename__ = "course"  # 表名
    id = models.Column(models.Integer, primary_key=True)  # 字段
    name = models.Column(models.String(32), unique=True)

Course_Student = models.Table(
    "course_student",
    models.Column("id",models.Integer,primary_key=True,autoincrement=True),
    models.Column('course_id',models.Integer,models.ForeignKey('course.id')),
    models.Column('student_id',models.Integer, models.ForeignKey('students.id')),
    models.Column('delete_flag', models.Integer,default=0) #0没有停课，1停课
)

models.drop_all()
models.create_all()




