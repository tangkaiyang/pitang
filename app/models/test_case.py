from app.models import db
from datetime import datetime


class TestCase(db.Model):
    id = db.Column(db.INT, primary_key=True)
    name = db.Column(db.String(32), unique=True, index=True)
    request_type = db.Column(
        db.INT, default=1, comment="请求类型1:http 2:grpc 3:dubbo")
    url = db.Column(db.TEXT, nullable=False, comment="请求url")
    request_method = db.Column(
        db.String(12), nullable=True, comment="请求方式,非http可为空")
    request_header = db.Column(db.TEXT, comment="请求头,可为空")
    # params = db.Coulmn(db.TEXT, comment="请求params")
    body = db.Column(db.TEXT, comment="请求body")
    project_id = db.Column(db.INT, comment="所属项目")
    tag = db.Column(db.String(64), comment="用例标签")
    status = db.Column(db.INT, comment="用例状态:1:待完成2:暂时关闭3:正常运作")
    priority = db.Column(db.String(3), comment="用例优先级:p0-p3")
    catalogue = db.Column(db.String(12), comment="用例目录")
    # expected = db.Column(db.TEXT, comment="预期结果,支持el表达式", nullable=False)
    created_at = db.Column(db.DATETIME, nullable=False)
    updated_at = db.Column(db.DATETIME, nullable=False)
    deleted_at = db.Column(db.DATETIME)
    create_user = db.Column(db.INT, nullable=True)
    update_user = db.Column(db.INT, nullable=True)

    def __init__(self, name, request_type, url, project_id, status, catalogue,  create_user, tag=None, priority="p3", request_header=None, body=None, request_method=None):
        self.name = name
        self.request_type = request_type
        self.url = url
        self.project_id = project_id
        self.tag = tag
        self.status = status
        self.priority = priority
        # self.catalogue = catalogue
        # self.expected = expected
        self.request_header = request_header
        # self.params = params
        self.body = body
        self.request_method = request_method
        self.created_at = datetime.now()
        self.updated_at = datetime.now()
        self.create_user = create_user
        self.update_user = create_user
        self.deleted_at = None
