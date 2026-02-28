import uuid
from dataclasses import dataclass
from typing import Optional

from injector import inject

from internal.model import App
from pkg.sqlalchemy import SQLAlchemy


@inject
@dataclass
class AppService:
    db: SQLAlchemy

    def create_app(self):
        with self.db.auto_commit():
            app = App()
            app.name = "测试应用"
            app.account_id = uuid.uuid4()
            app.icon = ""
            app.description = "第一个测试应用"
            self.db.session.add(app)
        return app

    def get_app(self, app_id: uuid.UUID) -> Optional[App]:
        """查看应用"""
        return self.db.session.query(App).filter(App.id == app_id).first()

    def update_app(
            self,
            app_id: uuid.UUID,
            name: Optional[str] = None,
            icon: Optional[str] = None,
            description: Optional[str] = None,
    ) -> Optional[App]:
        """更新应用"""
        app = self.get_app(app_id)
        if not app:
            return None

        with self.db.auto_commit():
            if name is not None:
                app.name = name
            if icon is not None:
                app.icon = icon
            if description is not None:
                app.description = description

        return app

    def delete_app(self, app_id: uuid.UUID) -> Optional[App]:
        """删除应用"""
        app = self.get_app(app_id)
        if not app:
            return None
        with self.db.auto_commit():
            self.db.session.delete(app)
        return app
