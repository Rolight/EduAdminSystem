# -*- coding: utf-8 -*-
#coding=utf-8
from flask import current_app
from flask_wtf import Form

from wtforms import StringField, PasswordField, BooleanField, SubmitField, SelectField, IntegerField, DateTimeField
from wtforms.validators import Length, Email, Regexp, EqualTo, DataRequired, NumberRange
from wtforms import ValidationError

from app.models.User import User, TeacherUser, StudentUser, DepartmentUser
from app.models.Department import Department, get_departments_choices_list
from app.models.Class import Class, get_classes_choices_list
from app.models.Major import Major, get_majors_choices_list


# 登录表单
class LoginForm(Form):
    username = StringField(u'学(工)号: ', validators=[DataRequired(), Length(1, 64)])
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


class StudentUserInformationForm(RegistrationForm):

    name = StringField(u'姓名*: ', validators=[DataRequired()])
    sex = SelectField(u'性别*: ', validators=[DataRequired()])
    nation = StringField(u'民族: ')
    public = StringField(u'政治面貌: ')
    # todo:身份证号可以加上正则表达式来判断是否合法
    idcard = StringField(u'身份证号: ')
    birthday = DateTimeField(u'出生年月(e.1995-07): ', format='%Y-%m')
    in_time = IntegerField(u'入学年份: ', validators=[DataRequired(), NumberRange(min=2000, max=2100, message=u'请输入大于2000并且小于2100的数字')])
    degree = SelectField(u'学位: ', validators=[DataRequired()])
    department = SelectField(u'院系*: ', validators=[DataRequired()], coerce=int)
    major = SelectField(u'专业*: ', validators=[DataRequired()], coerce=int)
    rclass = SelectField(u'班级*: ', validators=[DataRequired()], coerce=int)

    submit = SubmitField(u'注册')

    # 从外部加载选项
    def set_chioces(self):
        self.sex.choices = current_app.config['SEX']
        self.degree.choices = current_app.config['DEGREES']
        self.department.choices = get_departments_choices_list()
        self.major.choices = get_majors_choices_list()
        self.rclass.choices = get_classes_choices_list()

    # 验证专业
    def validate_major(self, field):
        major_id = field.data
        department_id = self.department.data
        if not Major.query.filter_by(id=major_id).first().department.id == department_id:
            raise ValidationError(u'院系和专业不匹配')

    # 验证班级
    def validate_rclass(self, field):
        major_id = self.major.data
        class_id = field.data
        if not Class.query.filter_by(id=class_id).first().major.id == major_id:
            raise ValidationError(u'专业和班级不匹配')



class TeacherUserInformationForm(RegistrationForm):

    name = StringField(u'姓名*: ', validators=[DataRequired()])
    sex = SelectField(u'性别*: ', validators=[DataRequired()])
    nation = StringField(u'民族: ')
    public = StringField(u'政治面貌: ')
    # todo:身份证号可以加上正则表达式来判断是否合法
    idcard = StringField(u'身份证号: ')
    birthday = DateTimeField(u'出生年月(e.1995-07): ', format='%Y-%m')
    in_time = IntegerField(u'入职年份: ', validators=[DataRequired(), NumberRange(min=1900, max=2100, message=u'请输入大于等于1900并且小于2100的数字')])
    degree = SelectField(u'职称*: ', validators=[DataRequired()])
    department = SelectField(u'院系*: ', validators=[DataRequired()], coerce=int)

    submit = SubmitField(u'注册')

    # 设置选项
    def set_chioces(self):
        self.sex.choices = current_app.config['SEX']
        self.degree.choices = current_app.config['TDEGREES']
        self.department.choices = get_departments_choices_list()





class DepartmentUserInformationForm(RegistrationForm):
    department = SelectField(u'院系: ', validators=[DataRequired()], coerce=int)

    submit = SubmitField(u'注册')

    def set_choices(self):
        self.department.choices = get_departments_choices_list()

