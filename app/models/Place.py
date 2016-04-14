# -*- coding: utf-8 -*-
#coding=utf-8


from app import db
from . import Major

class Place(db.Model):
    __tablename__ = 'places'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), nullable=False, unique=True)

    def __repr__(self):
        return '<class: %r>' % (self.name)