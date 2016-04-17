# -*- coding: utf-8 -*-
#coding=utf-8

from app import db
from . import Major

class TimeSpan(db.Model):
    __tablename__ = 'timespans'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), nullable=False, unique=True)
    arranges = db.relationship('Arrange', backref='timespan', lazy='dynamic')

    def __repr__(self):
        return '<class: %r>' % (self.name)