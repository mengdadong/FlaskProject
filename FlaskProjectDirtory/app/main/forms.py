import wtforms        #定义字段              #先继承了Form,na0.9时发生了改革，就导入俩了，
from flask_wtf import FlaskForm      #定义表单的父类
from wtforms import validators      #定义校验
# from models import Course
#form当中禁止查看数据库，数据库查询被认为是视图的功能
# course_list = [(c.id,c.label) for c in Course.query.all()]
course_list=[]

class TeacherForm(FlaskForm):
    """
    form字段的参数
    label=None, 表单的标签
    validators=None, 校验，传入校验的方法
    filters=tuple(), 过滤
    description='',  描述
    id=None, html id
    default=None, 默认值
    widget=None,
    render_kw=None,
    """
    name = wtforms.StringField("教师姓名",
                               render_kw = {
                                   "class":"form-control",
                                   "placeholder":"教师姓名"
                               },
                               validators = [
                                   validators.DataRequired("姓名不可以为空")       #不用担心validators冲突问题
                               ]
                               )

    age = wtforms.IntegerField("教师年龄",
                               render_kw={
                                   "class":"form-control",
                                   "placeholder":"教授年龄"
                               },
                               validators=[
                                   validators.DataRequired("年龄不可以为空")
                               ]
                               )
    gender = wtforms.SelectField("性别",
                                 choices=[("1","男"),
                                          ("1","女")
                                 ],
                                 render_kw={
                                     "class":"form-control",
                                     "placeholder":"教师性别"
                                 }
                                 )
    course = wtforms.SelectField("学科",          #Sel
                                choices=[
                                    ("1","Python"),     #为啥用元组：外面展示的
                                    ("2","PHP"),
                                    ("3","JAVA"),
                                    ("4","UI"),
                                    ("5","WEB")
                                ],
                                 render_kw={
                                     "class":"form-control",        #展示的样式
                                 }

                                )