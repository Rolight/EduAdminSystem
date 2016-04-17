# -*- coding: utf-8 -*-
#coding=utf-8

from flask import current_app
from flask_wtf import Form
from wtforms import StringField, SubmitField, TextAreaField, SelectField, FloatField
from wtforms.validators import DataRequired, Length

# 公告编辑表单
class PostForm(Form):
    title = StringField(u'公告标题', validators=[DataRequired(), Length(min=1, max=256)])
    body = TextAreaField(u'公告内容')
    submit = SubmitField(u'提交')

# 课程表单
class CourseForm(Form):
    code = StringField(u'课程代码', validators=[DataRequired(), Length(min=1, max=16)])
    name = StringField(u'课程名称', validators=[DataRequired(), Length(min=1, max=64)])
    nature = SelectField(u'课程性质', validators=[DataRequired()])
    credit = FloatField(u'学分', validators=[DataRequired()])
    description = TextAreaField(u'课程描述')
    submit = SubmitField(u'提交')

    # 设置课程性质选项
    def set_choices(self):
        self.nature.choices = current_app.config['COURSE_NATURE']

