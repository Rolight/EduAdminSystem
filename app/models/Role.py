# -*- coding: utf-8 -*-
#coding=utf-8

from app import db

# 用户权限分类
class Permission:
    # 超级管理员
    ADMIN = 0xff
    # 学生用户
    STUDENT = 0x01
    # 教师用户
    TEACHER = 0x02
    # 院系用户
    DEPARTMENT = 0x04

# 用户角色
class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(64), unique = True)
    default = db.Column(db.Boolean, default = False, index = True)
    permissions = db.Column(db.Integer)
    users = db.relationship('User', backref = 'role', lazy = 'dynamic')
    def __repr__(self):
        return '<Role %r>' % self.name

    # 往数据库中添加角色
    @staticmethod
    def create_base_role():
        # 一共四种角色，学生用户，教师用户，院系用户，超级管理员
        roles = {
            u'Student': (Permission.STUDENT, True),
            u'Department': (Permission.DEPARTMENT, False),
            u'Teacher': (Permission.TEACHER, False),
            u'Admin': (0xff, False),
        }
        for r in roles:
            role = Role.query.filter_by(name=r).first()
            if role is None:
                role = Role(name=r)
            role.permissions = roles[r][0]
            role.default = roles[r][1]
            db.session.add(role)
        db.session.commit()
