# -*- coding: utf-8 -*-
#coding=utf-8

from flask import current_app
from flask_wtf import Form
from wtforms import StringField, SubmitField, TextAreaField,\
    SelectField, FloatField, IntegerField, Label
from wtforms.validators import DataRequired, Length, NumberRange

from app.time import now_semaster, now_year
from app.models.Course import Course
from app.models.User import TeacherUser
from app.models.Place import Place
from app.models.TimeSpan import TimeSpan
from app.models.Arrange import Arrange, ArrangeTime

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


# 添加本学期课程安排
class ArrangeForm(Form):
    year = IntegerField(u'学年', validators=[DataRequired(), NumberRange(min=2000, max=2100)])
    semaster = IntegerField(u'学期', validators=[DataRequired(), NumberRange(min=1, max=3)])
    course = SelectField(u'课程', validators=[DataRequired()], coerce=int)
    teacher = SelectField(u'授课教师', validators=[DataRequired()], coerce=int)
    place = SelectField(u'上课地点', validators=[DataRequired()], coerce=int)
    all_timespan = []

    submit = SubmitField(u'添加课程安排')

    def set_choices(self, department_id):
        self.course.choices = \
            [(x.id, x.name) for x in Course.query.filter_by(department_id=department_id).all()]
        self.teacher.choices = \
            [(x.id, x.name) for x in TeacherUser.query.filter_by(department_id=department_id).all()]
        self.place.choices = \
            [(x.id, x.name) for x in Place.query.all()]

        self.year.data = now_year()
        self.semaster.data = now_semaster()


class ArrangeTimeSpanForm(Form):
    timespan = SelectField(u'上课时间', coerce=int)
    submit = SubmitField(u'添加时间')

    def set_choices(self, arrange_id):
        arrange = Arrange.query.filter_by(id=arrange_id).first()

        year = arrange.year
        semaster = arrange.semaster
        place_id = arrange.place_id

        occur_arranges = Arrange.query.filter_by(place_id=place_id).all()
        occur = []

        for occur_arrange in occur_arranges:
            for p in ArrangeTime.query.filter_by(id=occur_arrange.id).all():
                occur.append(p.timespan_id)

        all_time = [(x.id, x.name) for x in TimeSpan.query.all()]
        res = []
        for i in all_time:
            if i[0] not in occur:
                res.append(i)
        self.timespan.choices = res
