# -*- coding: utf-8 -*-
#coding=utf-8

from .. import db

# 用户角色
class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(64), unique = True)
    default = db.Column(db.Boolean, default = False, index = True)
    permissions = db.Column(db.Integer)
    users = db.relationship('User', backref = 'role', lazy = 'dynamic')
    def __repr__(self):
        return '<Role %r>' % self.name