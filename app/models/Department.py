# -*- coding: utf-8 -*-
#coding=utf-8

from app import db

class Department(db.Model):
    __tablename__ = 'departments'

    # 编号
    id = db.Column(db.Integer, primary_key=True)
    # 院系名称
    name = db.Column(db.String(64), nullable=False, unique=True)

    # 下属专业
    majors = db.relationship('Major', backref='department', lazy='dynamic')
    # 学生
    students = db.relationship('StudentUser', backref='department', lazy='dynamic')
    # 下属教师
    teachers = db.relationship('TeacherUser', backref='department', lazy='dynamic')
    # 院系管理员
    managers = db.relationship('DepartmentUser', backref='department', lazy='dynamic')
    # 下属课程
    courses = db.relationship('Course', backref='department', lazy='dynamic')
    # 下属课程安排
    arranges = db.relationship('Arrange', backref='department', lazy='dynamic')

    def __repr__(self):
        return '<Department: %r>' % self.name


def get_departments_choices_list():
    return [(dep.id, dep.name) for dep in Department.query.all()]


