# -*- coding: utf-8 -*-
#coding=utf-8

from flask import current_app
from flask_wtf import Form
from wtforms import SelectField, StringField, SubmitField
from wtforms.validators import Length, DataRequired
from wtforms import ValidationError

from app.models import Department, Major, Class

# 添加院系表单
class AddDepartmentForm(Form):
    name = StringField(u'院系名称', validators=[DataRequired(), Length(1, 32)])

    submit = SubmitField(u'添加')

    def validate_name(self, field):
        if Department.query.filter_by(name=field.name).first():
            raise ValidationError(u'院系名称已存在')


# 添加专业表单
class AddMajorForm(Form):

    name = StringField(u'专业名称', validators=[DataRequired(), Length(1, 32)])

    department_name = SelectField(u'所属学院', choices=Department.get_departments_choices_list(), validators=[DataRequired()], coerce=int)

    submit = SubmitField(u'添加')


    def validate_name(self, field):
        if Major.query_filter_by(name=field.name).first():
            raise ValidationError(u'专业已经存在')

# 添加班级表单
class AddClassForm(Form):

    name = StringField(u'班级名称', validators=[DataRequired(), Length(1, 32)])

    major_name = SelectField(u'所属专业', coerce=int, choices=Major.get_majors_choices_list(), validators=[DataRequired()])

    submit = SubmitField(u'添加')

    def validata_name(self, field):
        if Class.query.filter_by(name=field.name).first:
            raise ValidationError(u'班级名称已经存在')
