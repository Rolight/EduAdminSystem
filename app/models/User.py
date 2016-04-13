# -*- coding: utf-8 -*-
#coding=utf-8

from .. import db

from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin, login_required

# 用户
class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(64), unique = True)
    password_hash = db.Column(db.String(128))
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))

    def __repr__(self):
        return '<User %r, role %s>' % (self.name, self.role.name)

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)



from .. import login_manager
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))