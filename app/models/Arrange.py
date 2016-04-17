# -*- coding: utf-8 -*-
#coding=utf-8


from app import db

class Arrange(db.Model):
    __tablename__ = 'arranges'
    id = db.Column(db.Integer, primary_key=True)
    # 学年
    year = db.Column(db.Integer, nullable=False)
    # 学期
    semaster = db.Column(db.Integer, nullable=False)
    # 课程
    course_id = db.Column(db.Integer, db.ForeignKey('courses.id'), nullable=False)
    # 上课时间
    timespan_id = db.Column(db.Integer, db.ForeignKey('timespans.id'), nullable=False)
    # 上课地点
    place_id = db.Column(db.Integer, db.ForeignKey('places.id'), nullable=False)
    # 授课教师
    teacher_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

