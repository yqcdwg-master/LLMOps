import os

from flask import Flask
from flask_migrate import Migrate

from config import Config
from internal.exception import CustomException
from internal.router import Router
from pkg.response import json, Response, HttpCode
from pkg.sqlalchemy import SQLAlchemy


class Http(Flask):
    """http服务引擎"""

    def __init__(self,
                 *args,
                 conf: Config,
                 db: SQLAlchemy,
                 migrate: Migrate,
                 router: Router,
                 **kwargs
                 ):
        super(Http, self).__init__(*args, **kwargs)
        # 配置信息
        self.config.from_object(conf)

        # 注册自定义异常处理器
        self.register_error_handler(Exception, self._register_exception_handler)

        # 注册 sqlalchemy 扩展
        db.init_app(self)
        migrate.init_app(self, db=db, directory="internal/migrations")

        # # 初始化数据库
        # with self.app_context():
        #     _ = App()
        #     db.create_all()

        # 注册应用路由
        router.register_router(self)

    def _register_exception_handler(self, e: Exception):
        """注册自定义异常处理器"""
        # 1. 如果是自定义的异常，可以获取异常信息
        if isinstance(e, CustomException):
            return json(Response(
                code=e.code,
                message=e.message,
                data=e.data if e.data else {},
            ))

        # 2. 如果不是自定义异常，可能是程序中的未知异常，可以获取异常信息，状态码设置为 FAIL
        if self.debug or os.getenv("FLASK_ENV") == "development":
            raise e
        else:
            return json(Response(
                code=HttpCode.FAIL,
                message=str(e),
                data={}
            ))
