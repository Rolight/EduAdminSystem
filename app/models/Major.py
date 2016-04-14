# -*- coding: utf-8 -*-
#coding=utf-8

from app import db
from . import Department

class Major(db.Model):
    __tablename__ = 'majors'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True, nullable=False)

    department_id = db.Column(db.Integer, db.ForeignKey('departments.id'), nullable=False)
    # 下属班级
    classes = db.relationship('Class', backref='major', lazy='dynamic')
    # 下属学生
    students = db.relationship('StudentUser', backref='major', lazy='dynamic')

    def __repr__(self):
        return '<major: %r, department: %r>' % (self.name, self.department)


def get_majors_choices_list():
    return [(x.id, x.name) for x in Major.query.all()]

