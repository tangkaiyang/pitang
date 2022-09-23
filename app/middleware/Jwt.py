import hashlib
from datetime import timedelta, datetime

import jwt
from jwt.exceptions import ExpiredSignatureError

EXPIRED_HOUR = 3


class UserToken(object):
    key = 'pitangToken'
    salt = 'pitang'

    @staticmethod
    def get_token(data):
        new_data = dict({"exp": datetime.utcnow() +
                        timedelta(hours=EXPIRED_HOUR)}, **data)
        # return jwt.encode(new_data, key=UserToken.key).decode()
        return jwt.encode(new_data, key=UserToken.key)

    @staticmethod
    def parse_token(token):
        try:
            return jwt.decode(token, key=UserToken.key)
        except ExpiredSignatureError:
            raise Exception("token已过期, 请重新登录")

    @staticmethod
    def add_salt(password):
        m = hashlib.md5()
        bt = f"{password}{UserToken.salt}".encode("utf-8")
        m.update(bt)
        return m.hexdigest()
