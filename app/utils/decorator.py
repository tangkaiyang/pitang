'''
    这是一个装饰器方法文件
'''


from app import pitang
from functools import wraps
from flask import request, jsonify
from app.middleware.Jwt import UserToken

from jsonschema import validate, FormatChecker, ValidationError

FORBIDDEN = "对不起,你没有足够的权限"


class SingletonDecorator:
    def __init__(self, cls):
        self.cls = cls
        self.instance = None

    def __call__(self, *args, **kwds):
        if self.instance is None:
            self.instance = self.cls(*args, **kwds)
        return self.instance


def permission(role=pitang.config.get("GUEST")):
    def login_required(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            try:
                headers = request.headers
                token = headers.get("token")
                if token is None:
                    return jsonify(dict(code=400, msg="用户信息认证失败,请检查"))
                # print(token)
                user_info = UserToken.parse_token(token)
                kwargs["user_info"] = user_info

            except Exception as e:
                return jsonify(dict(code=401, msg=str(e)))
            # 判断用户权限
            if user_info.get("role", 0) < role:
                return jsonify(dict(code=400, msg=FORBIDDEN))
            return func(*args, **kwargs)
        return wrapper
    return login_required


def json_validate(sc):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            try:
                if request.get_json() is not None:
                    validate(request.get_json(), sc,
                             format_checker=FormatChecker())
                else:
                    raise Exception("请求JSON参数不合法")
            except ValidationError as e:
                return jsonify(dict(code=101, msg=str(e.message)))
            except Exception as e:
                return jsonify(dict(code=101, msg=str(e)))
            return func(*args, **kwargs)
        return wrapper
    return decorator
