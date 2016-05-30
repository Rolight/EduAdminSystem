# -*- coding: utf-8 -*-
#coding=utf-8
import os

basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    SECRET_KEY = os.environ.get('SECRET_KET') or 'hard to guess string'
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    SQLALCHEMY_TRACK_MODIFICATIONS = True

    host = '0.0.0.0'

    # 一些可能和学校相关的常量定义

    # 学位
    DEGREES = [(u'本科生', u'本科生'), (u'研究生', u'研究生'), (u'博士生', u'博士生')]

    # 教师职称
    TDEGREES = [(u'讲师', u'讲师'), (u'教授', u'教授')]

    # 性别
    SEX = [(u'男', u'男'), (u'女', u'女')]

    # 角色
    ROLES = [(1, u'本科生'), (2, u'研究生'), (3, u'博士生')]

    # 课程性质
    COURSE_NATURE = [(u'公共基础课', u'公共基础课'), (u'专业选修课', u'专业选修课'), (u'专业核心课', u'专业核心课')]

    # 超级管理员用户名
    ADMIN = u'admin'
    ADMIN_PASSWORD = u'loulinhui'

    @staticmethod
    def init_app(app):
        pass

class DevelopmentConfig(Config):
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DATABASE_URL') or 'sqlite:///' + os.path.join(basedir, 'data-dev.sqlite')
    #SQLALCHEMY_DATABASE_URI = 'mysql://root:loulinhui@localhost/eduAdminDev' + '?charset=utf8'



config = {
    'development': DevelopmentConfig,
    'default': DevelopmentConfig
}


