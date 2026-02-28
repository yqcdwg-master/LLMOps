from flask_migrate import Migrate
from injector import Injector

from config import config
from internal.router import Router
from internal.server import Http
from pkg.sqlalchemy import SQLAlchemy
from .module import ExtensionModule

injector = Injector([ExtensionModule])

app = Http(__name__,
           conf=config,
           db=injector.get(SQLAlchemy),
           migrate=injector.get(Migrate),
           router=injector.get(Router))
if __name__ == '__main__':
    app.run()
