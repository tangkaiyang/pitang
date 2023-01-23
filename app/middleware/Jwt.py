import hashlib
from datetime import timedelta, datetime

import jwt
from jwt.exceptions import ExpiredSignatureError

EXPIRED_HOUR = 3

# 信息编码成数据,数据解码成信息
# #e 中文编码成二进制数据,二进制数据解码成中文
# #d code指二进制码
# #e encode:str=>code


class UserToken(object):
    key = 'pitangToken'
    salt = 'pitang'

    @staticmethod
    def get_token(data):
        new_data = dict({"exp": datetime.utcnow() +
                        timedelta(hours=EXPIRED_HOUR)}, **data)
        # return jwt.encode(new_data, key=UserToken.key).decode()
        return jwt.encode(new_data, key=UserToken.key, algorithm="HS256")

    @staticmethod
    def parse_token(token):
        try:
            return jwt.decode(token, key=UserToken.key, algorithms=["HS256"])
        except ExpiredSignatureError:
            raise Exception("token已过期, 请重新登录")

    @staticmethod
    def add_salt(password):
        m = hashlib.md5()
        bt = f"{password}{UserToken.salt}".encode("utf-8")
        m.update(bt)
        return m.hexdigest()


if __name__ == "__main__":
    print(UserToken.parse_token("eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJleHAiOjE2NzQxODQwOTIsImlkIjoxLCJ1c2VybmFtZSI6InRhbmdreSIsIm5hbWUiOiJcdTZjNjRcdTk1MDUiLCJlbWFpbCI6Ijk0NTU0MTY5NkBxcS5jb20iLCJyb2xlIjowLCJjcmVhdGVkX2F0IjoiMjAyMi0wOS0yMyAwOTo1OTozMSIsInVwZGF0ZWRfYXQiOiIyMDIyLTA5LTIzIDA5OjU5OjMxIiwiZGVsZXRlZF9hdCI6bnVsbCwibGFzdF9sb2dpbl9hdCI6IjIwMjMtMDEtMjAgMDg6MDg6MTMifQ.PkvVd5mkatN3anHbNmkEesckOyWSp8q8WD9u-GjBxB0"))
