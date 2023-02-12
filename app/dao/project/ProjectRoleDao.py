from app.models import db
from app.models.project import Project
from app.models.project_role import ProjectRole
from app.utils.logger import Log
from app import pitang

from datetime import datetime


class ProjectRoleDao(object):
    log = Log("ProjectRoleDao")

    @staticmethod
    def list_project_by_user(user_id):
        """用户项目列表

        Args:
            user_id (string): 用户id

        Returns:
            list(project): 项目列表
        """
        try:
            projects = ProjectRole.query.filter(
                user_id=user_id, delete_at=None).all()
            return [p.id for p in projects], ""
        except Exception as e:
            ProjectRoleDao.log.error(f"查询用户{user_id}项目失败,{e}")
            return [], f"查询用户项目失败,{e}"

    @staticmethod
    def add_project_role(user_id, project_id, project_role, create_user):
        """为项目添加用户

        Args:
            user_id (int): 用户id
            project_id (int): 项目id
            project_role (int): 用户角色
            create_user (int): 创建人id
        """
        try:
            role = ProjectRole.query.filter(
                user_id=user_id, project_id=project_id, project_role=project_role, delete_at=None).first()
            if role is not None:
                return "用户已存在"
            role = ProjectRole(user_id=user_id, project_id=project_id,
                               project_role=project_role, create_user=create_user)
            db.session.add(role)
            db.session.commit()
        except Exception as e:
            ProjectRoleDao.log.error(f"添加用户失败,{e}")
            return f"添加用户失败,{e}"

    @staticmethod
    def list_role(project_id: int):
        try:
            roles = ProjectRole.query.filter_by(
                project_id=project_id, deleted_at=None).all()
            return roles, None
        except Exception as e:
            ProjectRoleDao.log.error(f"查询项目:{project_id}角色列表失败, {e}")
            return [], f"查询项目:{project_id}角色列表失败, {e}"

    @staticmethod
    def update_project_role(role_id, project_role, user, user_role):
        try:
            role = ProjectRole.query.filter_by(id=role_id, deleted_at=None).first()
            if role is None:
                return "该用户角色不存在"
            if user_role != pitang.config.get("ADMIN"):
                project = Project.query.filter_by(id=role.project_id).first()
                if project is None:
                    return "该项目不存在"
                if project.owner != user and role.project_role == 1:
                    # 说明既不是owner也不是超管，无法修改阻止的权限
                    return "不能修改其他组长的权限"
            updater_role = ProjectRole.query.filter_by(user_id=user, project_id=role.project_id,
                                                       deleted_at=None).first()
            if updater_role is None or updater_role.project_role == 1:
                return "对不起，你没有权限"
            role.project_role = project_role
            role.updated_at = datetime.now()
            role.update_user = user
            db.session.commit()
        except Exception as e:
            ProjectRoleDao.log.error(f"修改项目用户失败, {e}")
            return f"修改项目用户失败, {e}"
        return None

    @staticmethod
    def insert_project_role(user_id, project_id, project_role, user):
        ProjectRoleDao.add_project_role(user_id, project_id, project_role, user)
