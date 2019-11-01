from logging.handlers import RotatingFileHandler
import logging
from flask import Flask, session
from flask_session import Session
from flask_sqlalchemy import SQLAlchemy
from redis import StrictRedis
from flask_wtf.csrf import CSRFProtect
from config import config_dict

db = SQLAlchemy()
redis_store = None

def set_log(config_class):
    # 设置日志的记录等级
    logging.basicConfig(level=config_class.LOG_LEVEL)  # 调试debug级
    # 创建日志记录器，指明日志保存的路径、每个日志文件的最大大小、保存的日志文件个数上限 100M 最多可以记录10个日志文件
    file_log_handler = RotatingFileHandler("logs/log", maxBytes= 1024 * 1024 * 100, backupCount=10)
    # 创建日志记录的格式 日志等级 输入日志信息的文件名 行数 日志信息
    formatter = logging.Formatter('%(levelname)s %(filename)s:%(lineno)d %(message)s')
    # 为刚创建的日志记录器设置日志记录格式
    file_log_handler.setFormatter(formatter)
    # 为全局的日志工具对象（flask app使用的）添加日志记录器
    logging.getLogger().addHandler(file_log_handler)

# 将app的创建使用工厂模式封装起来
def create_app(config_name):
    app = Flask(__name__)
    config_class = config_dict[config_name]
    set_log(config_class)
    app.config.from_object(config_class)
    db.init_app(app)
    global redis_store
    redis_store = StrictRedis(host=config_class.REDIS_HOST,port=config_class.REDIS_PORT,db=config_class.REDIS_NUM)
    CSRFProtect(app)
    # 5.将session存储的数据从`内存`转移到`redis`中存储的
    Session(app)

    return app
