# -*- coding: utf-8 -*-
#coding=utf-8

from app import db

class Course(db.Model):

    __tablename__ = 'courses'

    id = db.Column(db.Integer, primary_key=True)

    # 课程代码
    code = db.Column(db.String(16), nullable=False)
    # 课程名称
    name = db.Column(db.String(64), nullable=False)
    # 课程性质
    nature = db.Column(db.String(64), nullable=False)
    # 学分
    credit = db.Column(db.Float, nullable=False)
    # 开课学院
    department_id = db.Column(db.Integer, db.ForeignKey('departments.id'), nullable=False)
    # 课程简介
    description = db.Column(db.Text)
    # 安排
    arranges = db.relationship('Arrange', backref='course', lazy='dynamic')
