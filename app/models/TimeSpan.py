# -*- coding: utf-8 -*-
#coding=utf-8

from app import db
from . import Major

class TimeSpan(db.Model):
    __tablename__ = 'timespans'

    # 编号
    id = db.Column(db.Integer, primary_key=True)
    # 名称
    name = db.Column(db.String(64), nullable=False, unique=True)

    arranges = db.relationship('ArrangeTime', backref='timespan', lazy='dynamic')

    def __repr__(self):
        return '<class: %r>' % (self.name)

    @staticmethod
    def add_default_timespan():
        weekday = [u'一', u'二', u'三', u'四', u'五', u'六', u'七']
        count = 0
        for day in weekday:
            for r in range(1, 12):
                timespan = TimeSpan(
                    id=count,
                    name=u'周%s 第%d节' % (day, r)
                )
                count += 1
                db.session.add(timespan)
                db.session.commit()


