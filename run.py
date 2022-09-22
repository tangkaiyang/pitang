from cmath import log
from app import pitang
from app.utils.logger import Log
from app import dao


@pitang.route('/')
def hello_world():
    log = Log("hello world专用")
    log.info("有人访问你的网站了")
    return 'Hello World!'


if __name__ == "__main__":
    pitang.run("0.0.0.0", threaded=True, port="7777")
