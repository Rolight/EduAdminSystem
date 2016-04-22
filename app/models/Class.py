# -*- coding: utf-8 -*-
#coding=utf-8

from app import db
from . import Major

class Class(db.Model):
    __tablename__ = 'classes'

    # 编号
    id = db.Column(db.Integer, primary_key=True)
    # 班级名称
    name = db.Column(db.String(64), nullable=False, unique=True)
    # 专业编号
    major_id = db.Column(db.Integer, db.ForeignKey('majors.id'), nullable=False)

    #下属学生
    students = db.relationship('StudentUser', backref='rclass', lazy='dynamic')

    def __repr__(self):
        return '<class: %r, major: %r>' % (self.name, self.major)


def get_classes_choices_list():
    return [(x.id, x.name) for x in Class.query.all()]

