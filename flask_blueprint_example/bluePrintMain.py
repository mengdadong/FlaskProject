"""
蓝图的官方案例
注册单一的蓝图实例
使用app加载蓝图
"""
from flask import Blueprint
from flask import Flask

simple_blueprint = Blueprint("simple_page",__name__)    #创建蓝图，将其实例化

@simple_blueprint.route("/")        #路由
def index():
    return "hello world"

#启动项目
if __name__ == '__main__':
    app = Flask(__name__)
    app.register_blueprint(simple_blueprint)    #注册蓝图
    app.run()