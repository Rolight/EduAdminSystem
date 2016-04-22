# -*- coding: utf-8 -*-
#coding=utf-8

from app import db


class Grades(db.Model):
    __tablename__ = "grades"

    student_id = db.Column(db.Integer, db.ForeignKey('users.id'), primary_key=True)
    arrange_id = db.Column(db.Integer, db.ForeignKey('arranges.id'), primary_key=True)
    grade = db.Column(db.Integer)


selectCourse = db.Table(
    'selectCourse',
    db.Column('student_id', db.Integer, db.ForeignKey('users.id')),
    db.Column('arrange_id', db.Integer, db.ForeignKey('arranges.id'))
)
