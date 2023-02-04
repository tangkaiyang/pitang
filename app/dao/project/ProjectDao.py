from sqlalchemy import or_

from app import pitang
from app.dao.project.ProjectRoleDao import ProjectRoleDao
from app.models import db
from app.models.project import Project
from app.utils.logger import Log
from datetime import datetime


class ProjectDao(object):
    log = Log("ProjectDao")

    @staticmethod
    def list_project(user, role, page, size, name=None):
        """获取项目列表

        Args:
            user (int): 用户id
            role (int): 角色id
            page (int): 页码
            size (int): 分页数
            name (string, optional): 项目名称. Defaults to None.
        """
        try:
            search = [Project.deleted_at == None]
            if role != pitang.config.get("ADMIN"):
                project_list, err = ProjectRoleDao.list_project_by_user(user)
                # if err is not None:
                #     raise Exception(err)
                search.append(or_(Project.id in project_list,
                                  Project.owner == user, Project.private == False))
            if name:
                search.append(Project.name.ilike("%{}%".format(name)))
            print(search)
            data = Project.query.filter(*search)
            total = data.count()
            return data.order_by(Project.created_at.desc()).paginate(page, per_page=size).items, total, None

        except Exception as e:
            ProjectDao.log.error(f"获取用户:{user}项目列表失败, {e}")
            return [], 0, f"获取用户:{user}项目列表失败,{e}"

    @staticmethod
    def add_project(name, owner, user, description, private):
        try:
            data = Project.query.filter_by(name=name, deleted_at=None).first()
            if data is not None:
                return "项目已存在"
            pr = Project(name, owner, user, description, private)
            db.session.add(pr)
            db.session.commit()
        except Exception as e:
            ProjectDao.log.error(f"新增项目:{name}失败,{e}")
            return f"新增项目: {name}失败, {e}"

    @staticmethod
    def query_project(project_id: int):
        try:
            data = Project.query.filter_by(id=project_id, deleted_at=None).first()
            if data is None:
                return None, [], "项目不存在"
            roles, err = ProjectRoleDao.list_role(project_id)
            if err is not None:
                return None, [], err
            return data, roles, None
        except Exception as e:
            ProjectDao.log.error(f"查询项目:{project_id}失败,{e}")
            return None, [], f"查询项目:{project_id}失败,{e}"

    @staticmethod
    def update_project(user, role, project_id, name, owner, private, description):
        """
        编辑项目
        :param user:
        :param role: 仅项目负责人和超级管理员可编辑项目
        :param project_id:
        :param name:
        :param owner:
        :param private:
        :param description:
        :return:
        """
        try:
            data = Project.query.filter_by(id=project_id, deleted_at=None).first()
            if data is None:
                return "项目不存在"
            # 仅项目负责人和超级管理员可编辑
            if data.owner != owner and role<pitang.config.get("ADMIN"):
                return "您没有权限修改项目负责人"
            data.name = name
            data.owner = owner
            data.private = private
            data.description = description
            data.updated_at = datetime.now()
            data.update_user = user
            db.session.commit()
        except Exception as e:
            msg = f"编辑项目:{name}失败,{e}"
            ProjectDao.log.error(msg)
            return msg


if __name__ == "__main__":
    print([Project.deleted_at == None])
