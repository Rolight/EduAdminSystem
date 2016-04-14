# -*- coding: utf-8 -*-
#coding=utf-8

from app import db

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

    __mapper_args__ = {
        'ploymorphic_identity':'user',
        'polymorphic_on':type
    }

    # 赋予角色
    def __init__(self):
        super()

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
    major_id = db.Column(db.Integer, db.ForeignKey('majors.id'))
    # 班级
    class_id = db.Column(db.Integer, db.ForeignKey('classes.id'))

    __mapper_args__ = {
        'ploymorphic_identity':'student',
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
    in_time = db.Column(db.Integer, nullable=False)
    # 职位
    degree = db.Column(db.String(10), nullable=False)
    # 院系
    department_id = db.Column(db.Integer, db.ForeignKey('departments.id'), nullable=False)

    __mapper_args__ = {
        'ploymorphic_identity':'teacher',
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
        'ploymorphic_identity':'department',
    }

    def __repr__(self):
        return '<department_user: %r>' % self.name




from .. import login_manager
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))