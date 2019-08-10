"""
flask-script  添加命令
"""

"""
flask script 官方案例
"""
from flask import Flask
from flask_script import Manager

app = Flask(__name__)

@app.route("/")
def index():
    return "Hello world"

manager = Manager(app)      #对app进行命令行序列化

@manager.command
def hello(name = "createsuperuser"):   #name是必须有的参数
    """
    :param name:  是命令行可以传递的参数，在命令行以 --name
    """
    username = input("please enter your username:")
    email = input("please enter your email:")
    password = input("please enter your password:")
    enter_password = input("please enter your username again:")
    return "哈哈哈，骗你呢，才不给你注册"

@manager.command
def runserver2(ip = "127.0.0.1",port = 8000):
    print("runserver in %s:%s"%(ip,port))

if __name__ == '__main__':
    manager.run()       #启动flask manage,manage 启动app
