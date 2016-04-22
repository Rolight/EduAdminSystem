# -*- coding: utf-8 -*-
#coding=utf-8

from flask import current_app
from app import db
from app.models.Role import Role, Permission
from app.models.Grades import Grades, selectCourse

from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin, login_required

# 用户
class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(64), unique = True)
    type = db.Column(db.String(50))
    password_hash = db.Column(db.String(128))

    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))

    # 公告
    posts = db.relationship('Post', backref='author', lazy='dynamic')

    # 安排
    arranges = db.relationship('Arrange', backref='teacher', lazy='dynamic')

    # 选课
    selected = db.relationship(
        'Arrange',
        secondary=selectCourse,
        backref=db.backref('students', lazy='dynamic'),
        cascade='all, delete-orphan',
        single_parent=True
    )

    __mapper_args__ = {
        'polymorphic_identity': 'user',
        'polymorphic_on': type
    }

    # 赋予角色
    def __init__(self, **kwargs):
        super(User, self).__init__(**kwargs)
        if self.role is None:
            if self.username == current_app.config['ADMIN']:
                self.role = Role.query.filter_by(permissions=0xff).first()
            if self.role is None:
                self.role = Role.query.filter_by(default=True).first()

    def __repr__(self):
        return '<User %r, role %s>' % (self.name, self.role.name)

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    # 判断用户是否拥有某个权限
    def can(self, permission):
        return self.role is not None and (self.role.permissions & permission) == permission

    # 是否是超级管理员
    def is_admin(self):
        return self.role.permissions == Permission.ADMIN

    # 是否是学生
    def is_student(self):
        return self.role.permissions == Permission.STUDENT

    # 是否是老师
    def is_teacher(self):
        return self.role.permissions == Permission.TEACHER

    # 是否是院系用户
    def is_department(self):
        return self.role.permissions == Permission.DEPARTMENT

    # 获取学生对象
    def get_student(self):
        return StudentUser.query.filter_by(id=self.id).first()

    # 获取教师对象
    def get_teacher(self):
        return TeacherUser.query.filter_by(id=self.id).first()

    # 获取院系对象
    def get_department(self):
        return DepartmentUser.query.filter_by(id=self.id).first()

# 三种用户类型，模型继承User类
# 学生用户
class StudentUser(User):
    __tablename__ = 'students'

    id = db.Column(db.Integer, db.ForeignKey('users.id'), primary_key=True)
    # 姓名
    name = db.Column(db.String(50), nullable=False)
    # 性别
    sex = db.Column(db.String(10), nullable=False)
    # 民族
    nation = db.Column(db.String(20))
    # 政治面貌
    public = db.Column(db.String(20))
    # 身份证号
    idcard = db.Column(db.String(30))
    # 出生年月
    birthday = db.Column(db.Date)
    # 入学年份
    in_time = db.Column(db.Integer, nullable=False)
    # 学位
    degree = db.Column(db.String(10), nullable=False)
    # 院系
    department_id = db.Column(db.Integer, db.ForeignKey('departments.id'), nullable=False)
    # 专业
    major_id = db.Column(db.Integer, db.ForeignKey('majors.id'), nullable=False)
    # 班级
    class_id = db.Column(db.Integer, db.ForeignKey('classes.id'), nullable=False)

    __mapper_args__ = {
        'polymorphic_identity': 'student',
    }

    def __repr__(self):
        return '<student: %r, %r %r %r>' % (self.name, self.department, self.major, self.rclass)

class TeacherUser(User):
    __tablename__ = 'teachers'

    # 姓名
    id = db.Column(db.Integer, db.ForeignKey('users.id'), primary_key = True)
    # 姓名
    name = db.Column(db.String(50), nullable=False)
    # 性别
    sex = db.Column(db.String(10), nullable=False)
    # 民族
    nation = db.Column(db.String(20))
    # 政治面貌
    public = db.Column(db.String(20))
    # 身份证号
    idcard = db.Column(db.String(30))
    # 出生年月
    birthday = db.Column(db.Date)
    # 入学年份
    in_time = db.Column(db.Integer)
    # 职位
    degree = db.Column(db.String(10), nullable=False)
    # 院系
    department_id = db.Column(db.Integer, db.ForeignKey('departments.id'), nullable=False)

    __mapper_args__ = {
        'polymorphic_identity': 'teacher',
    }

    def __repr__(self):
        return '<teacher: %r, %r>' % (self.name, self.department)

class DepartmentUser(User):
    __tablename__ = 'department_users'
    # id
    id = db.Column(db.Integer, db.ForeignKey('users.id'), primary_key = True)
    # 姓名
    name = db.Column(db.String(64))
    # 院系
    department_id = db.Column(db.Integer, db.ForeignKey('departments.id'))

    __mapper_args__ = {
        'polymorphic_identity': 'department',
    }

    def __repr__(self):
        return '<department_user: %r>' % self.name




from .. import login_manager
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

def add_administrator_user():
    admin = User(
        username=current_app.config['ADMIN'],
        password=current_app.config['ADMIN_PASSWORD']
    )
    db.session.add(admin)
    db.session.commit()
