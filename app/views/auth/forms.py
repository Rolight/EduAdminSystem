# -*- coding: utf-8 -*-
#coding=utf-8
from flask import current_app
from flask_wtf import Form
from wtforms import StringField, PasswordField, BooleanField, SubmitField, SelectField, DateTimeField
from wtforms.validators import Length, Email, Regexp, EqualTo, DataRequired, NumberRange
from wtforms import ValidationError
from app.models import Department, Major, Class

# 登录表单
class LoginForm(Form):
    username = StringField(u'学(工)号: ', validators=[DataRequired(), Length(1, 10)])
    password = PasswordField(u'密码', validators=[DataRequired()])
    remember_me = BooleanField(u'记住我')
    submit = SubmitField(u'登陆')


# 注册表单基类
# 这里可以添加正则表达式来判断学号是否合法
class RegistrationForm(Form):
    username = StringField(u'学(工)号: ', validators=[DataRequired(), Length(1, 64),
                                                   Regexp('^[A-Za-z][A-Za-z0-9_.]*$', 0, u'学工号只能含有字母数字和下划线')])
    password = PasswordField(u'密码: ', validators=[DataRequired(), EqualTo('password2', message=u'两次密码必须相等')])
    password2 = PasswordField(u'确认密码: ', validators=[DataRequired()])

    def validate_username(self, field):
        if User.query.filter_by(username = field.data).first():
            raise ValidationError(u'这个学工号已经被注册过了')

class StudentInformationForm(RegistrationForm):

    name = StringField(u'姓名: ', validators=[DataRequired()])
    sex = SelectField(u'性别: ', validators=[DataRequired()], choices=current_app.config['SEX'])
    nation = StringField(u'民族: ')
    public = StringField(u'政治面貌: ')
    # todo:身份可以加上正则表达式来判断是否合法
    idcard = StringField(u'身份证号: ')
    birthday = DateTimeField(u'出生年月: ')
    in_time = StringField(u'入学年份: ', validators=[DataRequired(), NumberRange(min=2000, max=2100, message=u'请输入大于2000并且小于2100的数字')])
    degree = SelectField(u'学位: ', validators=[DataRequired()], choices=current_app.config['DEGREES'])
    department = SelectField(u'院系: ', validators=[DataRequired()], choices=Department.get_departments_choices_list(), coerce=int)
    major = SelectField(u'专业: ', validators=[DataRequired()], choices=Major.get_majors_choices_list(), coerce=int)
    rclass = SelectField(u'班级: ', validators=[DataRequired()], choices=Class.get_classes_choices_list(), coerce=int)


    def validate_major(self):
        major_id = self.major.data
        department_id = self.department.data
        if not Major.query.filter_by(id=major_id).first().department.id == department_id:
            raise ValidationError(u'院系和专业不匹配')

    def validate_class(self):
        major_id = self.major.data
        class_id = self.rclass.data
        if not Class.query.filter_by(id=class_id).first().major.id == major_id:
            raise ValidationError(u'专业和班级不匹配')

