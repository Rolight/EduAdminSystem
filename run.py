# -*- coding: utf-8 -*-
#coding=utf-8
import os

from app import create_app, db

from flask_script import Manager, Shell
from flask_migrate import Migrate, MigrateCommand

from app.models.User import User, DepartmentUser, TeacherUser, StudentUser
from app.models.Class import Class
from app.models.Department import Department
from app.models.TimeSpan import TimeSpan
from app.models.Place import Place
from app.models.Major import Major
from app.models.Role import Role
from app.models.Post import Post
from app.models.Course import Course
from app.models.Arrange import Arrange
from app.models.Grades import Grades, selectCourse

# 导入默认配置文件
app = create_app(os.getenv('FLASK_CONFIG') or 'default')
manager = Manager(app)
# 数据库迁移
migrate = Migrate(app, db)

def make_shell_context():
    return dict(
        app=app,
        db=db,
        User=User,
        Role=Role,
        DepartmentUser=Department,
        TeacherUser=TeacherUser,
        StudentUser=StudentUser,
        Class=Class,
        Department=Department,
        TimeSpan=TimeSpan,
        Place=Place,
        Major=Major,
        Post=Post,
        Course=Course,
        Arrange=Arrange,
        Grades=Grades,
        selectCourse=selectCourse
    )

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

