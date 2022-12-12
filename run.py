from app import pitang
from app.utils.logger import Log
from app.controllers.auth.user import auth
from app.controllers.request.http import req
from app import dao

# 注册蓝图
pitang.register_blueprint(auth)
pitang.register_blueprint(req)


@pitang.route('/')
def hello_world():
    log = Log("hello world专用")
    log.info("有人访问你的网站了")
    return 'Hello World!'


if __name__ == "__main__":
    pitang.run("0.0.0.0", threaded=True, port="7777")
