from flask import Flask
from app.controllers.auth.user import auth
from config import Config

pitang = Flask(__name__)

# 注册蓝图
pitang.register_blueprint(auth)
pitang.config.from_object(Config)
