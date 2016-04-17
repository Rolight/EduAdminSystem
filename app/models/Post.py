# -*- coding: utf-8 -*-
#coding=utf-8

# 存放教务公告的数据模型
from flask import current_app

from app import db
from app.models.User import DepartmentUser, User
from datetime import datetime

class Post(db.Model):
    __tablename__ = 'posts'
    # 公告编号
    id = db.Column(db.Integer, primary_key=True)
    # 公告标题
    title = db.Column(db.String(480))
    # 公告内容
    body = db.Column(db.Text)
    # 公告时间
    post_time = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    # 发布者
    author_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    # 获取发布者
    def get_author_name(self):
        if self.author.name == current_app.config['ADMIN']:
            return u'超级管理员'
        else:
            return DepartmentUser.query.filter_by(id=self.author.id).first().department.name + u'学院'
