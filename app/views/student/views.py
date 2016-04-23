# -*- coding: utf-8 -*-
#coding=utf-8

from flask import render_template, redirect, request, url_for, flash, current_app, abort
from flask_login import login_required, current_user

from app import db
from app.decorators import student_required

from app.models.Arrange import Arrange, ArrangeTime
from app.models.Grades import Grades

from app.time import now_year, now_semaster

from . import student

# 管理已选课程
@student.route('/manager/selected')
@login_required
@student_required
def manager_selected():
    return render_template(
        'student/select_course_list.html',
        arranges=current_user.get_student().selected.all()
    )

# 显示可选课表
@student.route('/select/course')
@login_required
@student_required
def select_course_list():
    courses = []
    current_student = current_user.get_student()
    for arrange in Arrange.query.all():
        if arrange.year != now_year() or arrange.semaster != now_semaster():
            continue
        if arrange.department_id == current_student.department_id or arrange.course.nature == u'公共基础课':
            courses.append(arrange)
    return render_template(
        'student/select_course_list.html',
        arranges=courses
    )

# 选课
@student.route('/select/<int:id>')
@login_required
@student_required
def select_course(id):
    current_user.select_course(id)
    return redirect(url_for('student.select_course_list'))

# 退选
@student.route('/unselect/<int:id>')
@login_required
@student_required
def unselect_course(id):
    current_user.unselect_course(id)
    return redirect(url_for('student.select_course_list'))

# 查询课表
@student.route('/query/course/scedule')
@login_required
@student_required
def query_course_schedule():
    gtoi = {
        u"一": 1,
        u"二": 2,
        u"三": 3,
        u"四": 4,
        u"五": 5,
        u"六": 6,
        u"七": 7,
    }
    courses = current_user.get_student().selected.all()
    schedule = [ ['' for g in range(12)] for x in range(8)]
    for arrange in courses:
        # 去除不是本学期的课程
        if arrange.year != now_year() or arrange.semaster != now_semaster():
            continue
        for timespan in ArrangeTime.query.filter_by(id=arrange.id).all():
            name = timespan.timespan.name
            day, gid = gtoi[name[1]], int(name[4]) if not name[4:6].isdigit() else int(name[4:6])
            schedule[day][gid] = arrange.course.name + ' ' + arrange.place.name
    for i in range(1, 12):
        schedule[0][i] = u'第' + str(i) + u'节'
    return render_template(
        'student/course_schedule.html',
        schedule=schedule
    )

# 查询成绩
@student.route('/query/grade')
@login_required
@student_required
def query_grade():
    arranges = []
    for arrange in current_user.get_student().selected.all():
        if arrange.year == now_year() and arrange.semaster == now_semaster():
            arranges.append((arrange, Grades.query.filter_by(student_id=current_user.id, arrange_id=arrange.id).first().grade))
    return render_template(
        'student/query_grade.html',
        arranges=arranges
    )


