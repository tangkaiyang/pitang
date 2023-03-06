from app import pitang
from app.utils.logger import Log
from app.controllers.auth.user import auth
from app.controllers.request.http import req
from app.controllers.project.project import pr
from app.controllers.testcase.testcase import ts
from app import dao

# 注册蓝图
pitang.register_blueprint(auth)
pitang.register_blueprint(req)
pitang.register_blueprint(pr)
pitang.register_blueprint(ts)


@pitang.route('/')
def hello_world():
    log = Log("hello world专用")
    log.info("有人访问你的网站了")
    return 'Hello World!'


if __name__ == "__main__":
    pitang.run("0.0.0.0", threaded=True, port="7777", debug=True)
