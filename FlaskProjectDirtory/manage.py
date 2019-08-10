# 跑命令行
import os
from app import create_app, models
from flask_script import Manager        #需要使用这个插件
from flask_migrate import Migrate  # 用来同步数据库
from flask_migrate import MigrateCommand  # 用来同步数据库的命令

app = create_app("running")  # 实例化app

manager = Manager(app)  # 命令行进行封装

migrate = Migrate(app, models)  # 绑定可以管理的数据库模型，第一个是app，第二个参数是对哪个进行管理

manager.add_command("db", MigrateCommand)  # 加载数据库管理命令

if __name__ == '__main__':
    manager.run()
