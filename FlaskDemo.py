from flask import Flask
from flask import render_template #最基础的模板加载方法

app = Flask(__name__)
#__name__当前文件

@app.route("/index/",methods=["GET","POST"])  #路由，相当与django的urls
def hello_world():
    return "hello world"  #返回一个文本，最好返回json或者html页面

@app.route("/student/",methods=["GET","POST"])  #路由，相当与django的urls
def student():
    student_list = [
        {"name": "小明", "age": 18, "score": 70},
        {"name": "小红", "age": 18, "score": 75},
        {"name": "小强", "age": 15, "score": 80},
        {"name": "小刚", "age": 20, "score": 0},
        {"name": "小微", "age": 16, "score": 65},
        {"name": "tom", "age": 16, "score": 65},
    ]
    return render_template("students_list.html", **locals())

@app.route("/base/")
def base():
    return render_template("blank.html")

if __name__ == "__main__": #如果脚本自己执行
    app.run(host="0.0.0.0",port=8000,debug=True)