# -*- coding: utf-8 -*-
#coding=utf-8

from app import db


class Grades(db.Model):
    __tablename__ = "grades"
    id = db.Column(db.Integer, primary_key=True);
    student_id = db.Column(db.Integer, db.ForeignKey('students.id'))
    arrange_id = db.Column(db.Integer, db.ForeignKey('arranges.id'))
    grade = db.Column(db.Integer)


selectCourse = db.Table(
    'selectCourse',
    db.Column('student_id', db.Integer, db.ForeignKey('students.id')),
    db.Column('arrange_id', db.Integer, db.ForeignKey('arranges.id'))
)
