import os

import pymysql
from flask import Flask
from flask import render_template

from flask_sqlalchemy import SQLAlchemy

pymysql.install_as_MySQLdb()

app = Flask(__name__)
BASE_DIR = os.path.abspath(os.path.dirname(__file__))

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///"+os.path.join(BASE_DIR,"Student.sqlite")
# app.config["SQLALCHEMY_DATABASE_URI"] = "mysql://root:123@localhost/school"
app.config["SQLALCHEMY_COMMIT_ON_TEARDOWN"] = True
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True

models = SQLAlchemy(app) #关联sqlalchemy和flask应用

session = models.session()

class BaseModel(models.Model):
    __abstract__ = True #抽象表为True，代表当前类为抽象类，不会被创建
    id = models.Column(models.Integer, primary_key=True, autoincrement=True)

    def save(self):
        session.add(self)
        session.commit()
    def delete_obj(self):
        session.delete(self)
        session.commit()
#
class Students(BaseModel):
    """
    学员表
    """
    __tablename__ = "students"
    name = models.Column(models.String(32))
    age = models.Column(models.Integer)
    gender = models.Column(models.Integer,default = 13) #0 男 1女 -1 unknown


Stu_Cou = models.Table(
    "stu_cou",
    models.Column("id", models.Integer, primary_key=True, autoincrement=True),
    models.Column("course_id", models.Integer, models.ForeignKey("course.id")),
    models.Column("student_id", models.Integer, models.ForeignKey("students.id"))
)


class Course(BaseModel):
    """
    课程表
    """
    __tablename__ = "course"
    label = models.Column(models.String(32))
    description = models.Column(models.Text)

    to_teacher = models.relationship(
        "Teachers",  #映射表
        backref = "to_course_data", #反向映射字段，反向映射表通过该字段查询当前表内容
    ) #指向映射表字段

    to_student = models.relationship(
        "Students",
        secondary = Stu_Cou,
        backref = models.backref("to_course",lazy = "dynamic"), #stu_cou course
        lazy = "dynamic" #stu_cou student
        #select 访问该字段时候，加载所有的映射数据
        #joined  对关联的两个表students和stu_cou进行join查询
        #dynamic 不加载数据
    )


class Attendance(BaseModel):
    """
    考勤表，记录是否请假
    学员
    """
    __tablename__ = "attendance"
    att_time = models.Column(models.Date)
    status = models.Column(models.Integer,default = 1) #0 迟到  1 正常出勤  2 早退  3 请假  4 旷课
    student_id = models.Column(models.Integer, models.ForeignKey("students.id"))


class Grade(BaseModel):
    """
    成绩表
    课程，学员关联此表
    """
    __tablename__ = "grade"
    grade = models.Column(models.Float, default=0)
    course_id = models.Column(models.Integer, models.ForeignKey("course.id"))
    student_id = models.Column(models.Integer, models.ForeignKey("students.id"))


class Teachers(BaseModel):
    """
    教师
    老师与课程是多对一关系
    """
    __tablename__ = "teachers"
    name = models.Column(models.String(32))
    age = models.Column(models.Integer)
    gender = models.Column(models.Integer,default = 3)  # 0 男 1女 -1 unknown
    course_id = models.Column(models.Integer, models.ForeignKey("course.id")) #教师多对一 映射表是课程

@app.route("/student_list/")
def student_list():
    students = Students.query.all()
    return render_template("students_list.html",**locals())


if __name__ == "__main__":
    app.run()































# models.drop_all()
# models.create_all()
# #定义两个课程
# course = Course()
# course.label = "python"
# course.description = "python"
# course.save()
#
# course1 = Course()
# course1.label = "php"
# course1.description = "php"
# course1.save()
# #定义两个学员
# s = Students()
# s.name = "小明"
# s.age = 13
# s.gener = 0
# s.save()
#
# s1 = Students()
# s1.name = "小刘"
# s1.age = 13
# s1.gener = 0
# s1.save()
# #保存关联
# s.to_course = [course]
# s.save()
# s1.to_course = [course,course1]
# s1.save()
#
#
# student = Students.query.get(1)
# print(student.to_course.all()) #查询id为1的学员的所有课程
#
# coures = Course.query.get(1)
# print(coures.to_student.all()) #查询id为1的课程的所有有学员




# models.drop_all()
# models.create_all()
#
# course = Course()
# course.label = "python"
# course.description = "python"
# course.save()
#
# teacher = Teachers()
# teacher.name = "lb"
# teacher.age = 18
# teacher.gender = 0
# teacher.course_id = course.id
# teacher.save()
#
# teacher = Teachers()
# teacher.name = "ll"
# teacher.age = 18
# teacher.gender = 0
# teacher.course_id = course.id
# teacher.save()
#
#
# t = Teachers.query.get(1)
# print(t.to_course_data)
# c = Course.query.get(1)
# print(c.to_teacher)

#
# #++++++++++++++++++++++++++++++++++++++++++++++++
# cou = Course()
# cou.label = "python"
# cou.description = "python"
# cou.save()
#
# course1 = Course()
# course1.label = "php"
# course1.description = "php"
# course1.save()
#
# s = Students()
# s.name = "小明"
# s.age = 13
# s.gener = 0
# s.save()
#
# s1 = Students()
# s1.name = "小刘"
# s1.age = 13
# s1.gener = 0
# s1.save()
#
# s.to_course = [cou]
# s.save()
# s1.to_course = [cou,course1]
# s1.save()
#
#
# student = Students.query.get(1)
# print(student.to_course.all())
#
# coures = Course.query.get(1)
# print(coures.to_student.all())




#查询
# teachers = Teachers.query.all() #查询所有数据
# print(teachers)
# teachers = Teachers.query.first() #查询所有数据第一个
# print(teachers)
# teachers = Teachers.query.all()[:2] #返回前2条
# print(teachers)
# teachers = Teachers.query.filter_by(age = 18).all() #返回过滤之后的所有结果
# print(teachers)
# teachers = Teachers.query.filter_by(age = 18).first() #返回过滤之后的第一个结果
# print(teachers)
# teachers = Teachers.query.order_by("age").all() #返回升序排序之后的所有结果
# print(teachers)
# teachers = Teachers.query.order_by(models.desc("age")).all() #返回降序排序之后的所有结果
# print(teachers)
# teacher = Teachers.query.get(4) #get以主键作为条件
# print(teacher)
# teachers = Teachers.query.offset(1).limit(2).all() #返回前2条
#     #offset 偏移
#     #limit 限制条数
#     #从第一条开始查询查询2条
# print(teachers)


"""
 'add_column', 'add_columns
', 'add_entity', 'all', 'as_scalar', 'autoflush', 'column_descriptions', 'correlate', 'count', 'cte', 'delete', 'dispatch', 'disti
nct', 'enable_assertions', 'enable_eagerloads', 'except_', 'except_all', 'execution_options', 'exists', 'filter', 'filter_by', 'fi
rst', 'first_or_404', 'from_self', 'from_statement', 'get', 'get_execution_options', 'get_or_404', 'group_by', 'having', 'instance
s', 'intersect', 'intersect_all', 'join', 'label', 'lazy_loaded_from', 'limit', 'logger', 'merge_result', 'offset', 'one', 'one_or
_none', 'only_return_tuples', 'options', 'order_by', 'outerjoin', 'paginate', 'params', 'populate_existing', 'prefix_with', 'reset
_joinpoint', 'scalar', 'select_entity_from', 'select_from', 'selectable', 'session', 'slice', 'statement', 'subquery', 'suffix_wit
h', 'union', 'union_all', 'update', 'value', 'values', 'whereclause', 'with_entities', 'with_for_update', 'with_hint', 'with_label
s', 'with_lockmode', 'with_parent', 'with_polymorphic', 'with_session', 'with_statement_hint', 'with_transformation', 'yield_per']
"""
# t = Teachers.query.get(1)
# print(t.name)
# t.name = "老边好帅"
# session.add(t)
# session.commit()
#
# t = Teachers.query.get(1)
# print(t.name)
# t.name = "老边好帅"
# t.save()

# Teachers.query.get(2).delete_obj()





# t = Teachers(name = "老边",age = 18,gender = "男",course_id = 1)
# t1 = Teachers()
# t1.name = "老王"
# t1.age = 48
# t1.gender = "男"
# t1.course_id = 1
# d2 = {"name": "老白","age": 38, "gender": "女","course_id": 1}
# t2 = Teachers(**d2)
# session.add_all([t,t1,t2])
# session.commit()

# models.drop_all()
# models.create_all()

# course = Course()
# course.label = "php"
# course.description = "php"
# course.save()

# teacher = Teachers()
# teacher.name = "老王"
# teacher.age = 18
# teacher.gender = 0
# teacher.course_id = 1
# teacher.save()

# students = Students()
# students.name = 9527
# students.age = 18
# students.save()


# session = models.session() #创建一个数据库修改实例 增删改
# course = Course(label = "linux",description = "关机，重启，拔电源")
# course1 = Course(label = "php",description = "世界上最好的语言")
# session.add_all([course,course1])
# course = Course()
# course.label = "java"
# course.description = "美酒加咖啡"
# course.save()


# models.drop_all()
# models.create_all()

# page = 1
# page_size = 10
# start = (page-1)*page_size
# teachers = Teachers.query.offset(start).limit(page_size).all()










