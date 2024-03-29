from flask import Blueprint, jsonify, request

from app import pitang
from app.dao.project.ProjectDao import ProjectDao
from app.dao.project.ProjectRoleDao import ProjectRoleDao
from app.handler.factory import ResponseFactory
from app.handler.page import PageHandler
from app.utils.decorator import permission

# 通过Blueprint注册到flask
pr = Blueprint("project", __name__, url_prefix="/project")


# 定义路径


@pr.route("/list")
@permission()
def list_project(user_info):
    """获取项目列表

    Args:
        user_info (dict): 用户信息
    """
    page, size = PageHandler.page()
    user_role, user_id = user_info["role"], user_info["id"]
    name = request.args.get("name")
    # todo 返回total
    result, total, err = ProjectDao.list_project(
        user_id, user_role, page, size, name)
    if err is not None:
        return jsonify(dict(code=110, data=result, msg=err))
    return jsonify(dict(code=0, data=ResponseFactory.model_to_list(result), msg="操作成功"))


@pr.route("/insert", methods=["POST"])
@permission(pitang.config.get("MANAGER"))
def insert_project(user_info):
    """添加项目

    Args:
        user_info (dict): 用户信息
    """
    try:
        user_id = user_info["id"]
        data = request.get_json()
        if not data.get("name") or not data.get("owner"):
            return jsonify(dict(code=101, msg="项目名称/负责人不能为空"))
        if not data.get("app", ""):
            return jsonify(dict(code=101, msg="服务名称不能为空"))
        private = data.get("private", False)
        err = ProjectDao.add_project(
            data.get("name"), data.get("app"), data.get("owner"), user_id, data.get("description", ""), private)
        if err is not None:
            return jsonify(dict(code=101, msg=str(err)))
        return jsonify(dict(code=0, msg="操作成功"))
    except Exception as e:
        return jsonify(dict(code=111, msg=str(e)))


@pr.route("/query")
@permission()
def query_project(user_info):
    project_id = request.args.get("projectId")
    if project_id is None or not project_id.isdigit():
        return jsonify(dict(code=101, msg="请传入正确的projectId"))
    result = dict()
    data, roles, tree, err = ProjectDao.query_project(project_id)
    if err is not None:
        return jsonify(dict(code=110, data=result, msg=err))
    result.update({"project": ResponseFactory().model_to_dict(
        data), "roles": ResponseFactory.model_to_list(roles), "test_case": tree})
    return jsonify(dict(code=0, data=result, msg="操作成功"))


@pr.route("/update", methods=["POST"])
@permission()
def update_project(user_info):
    try:
        user_id, role = user_info["id"], user_info["role"]
        data = request.get_json()
        if data.get("id") is None:
            return jsonify(dict(code=101, msg="项目id不能为空"))
        if data.get("name") is None or data.get("owner") is None:
            return jsonify(dict(code=101, msg="项目名称/项目负责人不能为空"))
        if not data.get("app", ""):
            return jsonify(dict(code=101, msg="服务名称不能为空"))
        private = data.get("private", False)
        err = ProjectDao.update_project(user_id, role, data.get("id"), data.get("name"), data.get("app"), data.get("owner"), private,
                                        data.get("description", ""))
        if err is not None:
            return jsonify(dict(code=110, msg=err))
        return jsonify(dict(code=0, msg="操作成功"))
    except Exception as e:
        return jsonify(dict(code=111, msg=str(e)))


@pr.route("/role/insert", methods=["POST"])
@permission()
def insert_project_role(user_info):
    try:
        data = request.get_json()
        if data.get("user_id") is None or data.get("project_role") is None or data.get("project_id") is None:
            return jsonify(dict(code=101, msg="请求参数有误"))
        err = ProjectRoleDao.insert_project_role(data.get("user_id"), data.get(
            "project_id"), data.get("project_role"), user_info["id"])
        if err is not None:
            return jsonify(dict(code=110, msg=err))
    except Exception as e:
        return jsonify(dict(code=110, msg=str(e)))
    return jsonify(dict(code=0, msg="操作成功"))


@pr.route("/role/update", methods=["POST"])
@permission()
def update_project_role(user_info):
    try:
        data = request.get_json()
        if data.get("user_id") is None or data.get("project_role") is None or data.get("project_id") is None \
                or data.get("id") is None:
            return jsonify(dict(code=101, msg="请求参数有误"))
        err = ProjectRoleDao.update_project_role(data.get("id"), data.get("project_role"),
                                                 user_info["id"], user_info["role"])
        if err is not None:
            return jsonify(dict(code=110, msg=err))
    except Exception as e:
        return jsonify(dict(code=110, msg=str(e)))
    return jsonify(dict(code=0, msg="操作成功"))


if __name__ == '__main__':
    a = "1"
    print(a.isdigit())
