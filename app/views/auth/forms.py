# -*- coding: utf-8 -*-
#coding=utf-8
from flask_wtf import Form
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import Required, Length, Email, Regexp, EqualTo
from wtforms import ValidationError
from app.models import User

class LoginForm(Form):
    username = StringField(u'学(工)号: ', validators=[Required(), Length(1, 10)])
    password = PasswordField(u'密码', validators=[Required()])
    remember_me = BooleanField(u'记住我')
    submit = SubmitField(u'登陆')


# 这里可以添加正则表达式来判断学号是否合法
class RegistrationForm(Form):
    username = StringField(u'学(工)号: ', validators=[Required(), Length(1, 64),
                                                   Regexp('^[A-Za-z][A-Za-z0-9_.]*$', 0, u'学工号只能含有字母数字和下划线')])
    password = PasswordField(u'密码: ', validators=[Required(), EqualTo('password2', message=u'两次密码必须相等')])
    password2 = PasswordField(u'确认密码: ', validators=[Required()])
    submit = SubmitField('Register')

    def validate_username(self, field):
        if User.query.filter_by(username = field.data).first():
            raise ValidationError('这个学工号已经被注册过了')
