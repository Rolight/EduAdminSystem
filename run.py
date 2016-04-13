# -*- coding: utf-8 -*-
#coding=utf-8
import os

from app import create_app, db
from app.models import User, Role
from flask_script import Manager, Shell
from flask_migrate import Migrate, MigrateCommand

# 导入默认配置文件
app = create_app(os.getenv('FLASK_CONFIG') or 'default')
manager = Manager(app)
# 数据库迁移
migrate = Migrate(app, db)

def make_shell_context():
    return dict(app = app, db = db, User = User, Role = Role)

manager.add_command("shell", Shell(make_context=make_shell_context))
manager.add_command('db', MigrateCommand)

# run the unit test
@manager.command
def test():
    import unittest
    test = unittest.TestLoader().discover('tests')
    unittest.TextTestRunner(verbosity=2).run(test)


if __name__ == '__main__':
    manager.run()

