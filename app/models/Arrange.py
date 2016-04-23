# -*- coding: utf-8 -*-
#coding=utf-8


from app import db
from app.models.Grades import Grades, selectCourse

class Arrange(db.Model):
    __tablename__ = 'arranges'
    # 编号
    id = db.Column(db.Integer, primary_key=True)
    # 学年
    year = db.Column(db.Integer, nullable=False)
    # 院系
    department_id = db.Column(db.Integer, db.ForeignKey('departments.id'), nullable=False)
    # 学期
    semaster = db.Column(db.Integer, nullable=False)
    # 课程
    course_id = db.Column(db.Integer, db.ForeignKey('courses.id'), nullable=False)
    # 授课教师
    teacher_id = db.Column(db.Integer, db.ForeignKey('teachers.id'), nullable=False)
    # 上课地点
    place_id = db.Column(db.Integer, db.ForeignKey('places.id'), nullable=False)

    # 选了这门课程的学生
    student = db.relationship(
        'StudentUser',
        secondary=selectCourse,
        backref=db.backref('selects', lazy='dynamic'),
        cascade='all, delete-orphan',
        single_parent=True,
        lazy='dynamic'
    )

    # 获取上课时间
    def get_timespan(self):
        timespans = ArrangeTime.query.filter_by(id = self.id).all()
        ret = ""
        for timespan in timespans:
            ret += timespan.timespan.name + " "
        return ret

class ArrangeTime(db.Model):
    __tablename__ = 'arrangetimes'
    # 编号
    id = db.Column(db.Integer, db.ForeignKey('arranges.id'), primary_key=True)
    # 上课时间
    timespan_id = db.Column(db.Integer, db.ForeignKey('timespans.id'), nullable=False, primary_key=True)

