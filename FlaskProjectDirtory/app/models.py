"""
m模型

"""
from app import models

      #创建一个数据库修改实例，增删改

class BaseModel(models.Model):
    __abstract__ = True  #抽象表为True，代表当前类为抽象类
    id = models.Column(models.Integer,primary_key=True,autoincrement=True)

    def save(self):  #插入数据
        db = models.session()
        db.add(self)
        db.commit()

    def delete_obj(self):
        db = models.session()
        db.delete(self)
        db.commit()

class User(BaseModel):
    __tablename__ = "user"
    username = models.Column(models.String(32))
    password = models.Column(models.String(32))
    identity = models.Column(models.Integer)    #0学员  1教师
    identity_id = models.Column(models.Integer,nullable=True)

class Students(BaseModel):
    """
    学员表
    """
    __tablename__ = "students"      #mysql不区分大小写，但是SQL是去区分的
    id = models.Column(models.Integer,primary_key=True,autoincrement=True)
    name = models.Column(models.String(32))
    age = models.Column(models.Integer)
    gender = models.Column(models.Integer)  #0男 1女 -1未知

# class Stu_Cou(BaseModel):
#     """
#     课程，学员关联表
#     """
#     __tablename__ = "stu_cou"
#     id = models.Column(models.Integer,primary_key=True,autoincrement=True)
#     course_id = models.Column(models.Integer,models.ForeignKey("course.id"))
#     student_id = models.Column(models.Integer,models.ForeignKey("students.id"))
Stu_Cou = models.Table(
    "stu_cou",
    models.Column("id",models.Integer,primary_key=True,autoincrement=True),
    models.Column("course_id",models.Integer,models.ForeignKey("course.id")),
    models.Column("student_id",models.Integer,models.ForeignKey("students.id"))
)

class Course(BaseModel):
    """
    课程表
    """
    __tablename__ = "course"
    id = models.Column(models.Integer,primary_key=True,autoincrement=True)
    label = models.Column(models.String(32))
    description = models.Column(models.Text)

    to_teacher = models.relationship(       #当前字段用于一对多或者多对一反向映射
        "Teachers",#映射模型的名称
        backref = "to_course_data"        #反向引用---反向映射字段，反向映射表通过改字段查询当前表内容
    )#指向映射表字段

    to_student = models.relationship(
        "Students",
        secondary = Stu_Cou,
        backref = models.backref("to_course",lazy = "dynamic"),     #lazy与on_delete作用一样，有固定参数，类似默认值的意思
        lazy = "dynamic"
    )
    #select 访问该字段时候，加载所有的映射数据
    #joined  对关联的两个表students和stu_cou进行join查询
    #dynamic 不加载数据



class Grade(BaseModel):
    """
    成绩表
    课程，学员关联表
    """
    __tablename__ = "grade"
    id = models.Column(models.Integer,primary_key=True,autoincrement=True)
    grade = models.Column(models.Float,default=0)
    course_id = models.Column(models.Integer,models.ForeignKey("course.id"))
    student_id = models.Column(models.Integer,models.ForeignKey("students.id"))

class Attendance(BaseModel):
    """
    考勤表，记录是否请假
    学员
    """
    __tablename__ = "attendance"
    id = models.Column(models.Integer,primary_key=True,autoincrement=True)
    att_time = models.Column(models.Date)       #在涉及时间时不用time，因为时关键字
    status = models.Column(models.Integer)  #0 迟到  1正常出勤  2 早退   3 请假
    student_id = models.Column(models.Integer,models.ForeignKey("students.id"))

class Teachers(BaseModel):
    """
    教师
    老师与课程是一对一关系
    """
    __tablename__ = "teachers"
    id = models.Column(models.Integer,primary_key=True,autoincrement=True)
    name = models.Column(models.String(32))
    age = models.Column(models.Integer)
    gender = models.Column(models.Integer)  #0 男 1 女 -1 unknow
    course_id = models.Column(models.Integer,models.ForeignKey("course.id"))

# models.create_all()