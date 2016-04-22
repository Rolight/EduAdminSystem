# -*- coding: utf-8 -*-
#coding=utf-8


from app import db
from . import Major

class Place(db.Model):
    __tablename__ = 'places'

    # 编号
    id = db.Column(db.Integer, primary_key=True)
    # 上课地点名称
    name = db.Column(db.String(64), nullable=False, unique=True)

    arranges = db.relationship('Arrange', backref='place', lazy='dynamic')

    def __repr__(self):
        return '<class: %r>' % (self.name)