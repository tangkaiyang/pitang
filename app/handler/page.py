from flask import request

# 默认页码和页数
PAGE = 1
SIZE = 10


class PageHandler(object):
    @staticmethod
    def page():
        """获取page和size

        Returns:
            tuple: page,size元组
        """
        page = request.args.get("page")
        if page is None or not page.isdigit():
            page = PAGE
        size = request.args.get("size")
        if size is None or not size.isdigit():
            size = SIZE
        return int(page), int(size)