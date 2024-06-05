from flask import Blueprint
from flask import jsonify
from flask import request
from app.utils.decorator import permission
from app.utils.executor import Executor

from app.middleware.HttpClient import Request
from app.middleware.MyRedis import MyRedis

from app.enums import RedisEnum

req = Blueprint("request", __name__, url_prefix="/request")


@req.route("/http", methods=['POST'])
@permission()
def http_request(user_info):
    data = request.get_json()
    method = data.get("method")
    if not method:
        return jsonify(dict(code=101, msg="请求方式不能为空"))
    url = data.get("url")
    if not url:
        return jsonify(dict(code=101, msg="请求地址不能为空"))
    body = data.get("body")
    headers = data.get("headers")
    r = Request(url, data=body, headers=headers)
    my_redis = MyRedis()
    my_redis.set(RedisEnum.REQUEST_HISTORY + str(url), str(url) + str(body) + str(headers))
    response = r.request(method)
    if response.get("status"):
        return jsonify(dict(code=0, data=response, msg="操作成功"))
    return jsonify(dict(code=110, data=response, msg=response.get("msg")))


@req.route("/run")
@permission()
def execute_case(user_info):
    case_id = request.args.get("case_id")
    if not case_id or not case_id.isdigit():
        return jsonify(dict(code=101, msg="传入用例id有误"))
    result, err = Executor.run(case_id)
    if err:
        return jsonify(dict(code=110, data=result, msg=err))
    return jsonify(dict(code=0, data=result, msg="操作成功"))


@req.route("/history")
@permission()
def query_history(user_info):
    case_id = request.args.get("case_id")
    if not case_id or not case_id.isdigit():
        return jsonify(dict(code=101, msg="传入用例id有误"))
    result, err = Executor.run(case_id)
    if err:
        return jsonify(dict(code=110, data=result, msg=err))
    return jsonify(dict(code=0, data=result, msg="操作成功"))


@req.route("/test", methods=['POST'])
def is_auto_transfer():
    data = request.get_json()
    product_tags = data.get("productTags")
    if not product_tags or len(product_tags) == 0:
        return jsonify(dict(code=400, msg="productTags不能为空"))
    taxNum = data.get("taxNum")
    if not taxNum:
        return jsonify(dict(code=400, msg="taxNum不能为空"))
    if taxNum == "91330104TKYTEST001":
        auto_transfer = 1
    else:
        auto_transfer = 0
    data = []
    for tag in product_tags:
        data.append({
            "productTag": tag,
            "isAutoTransfer": auto_transfer
        })
    return jsonify(dict(result=None, code=200, message="成功", data=data))
