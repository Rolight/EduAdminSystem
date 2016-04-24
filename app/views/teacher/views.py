# -*- coding: utf-8 -*-
#coding=utf-8

from flask import render_template, redirect, request, url_for, flash, current_app, abort
from flask_login import login_required, current_user

from app import db
from app.decorators import teacher_required
from app.models.Arrange import Arrange, ArrangeTime
from app.models.User import User, StudentUser, TeacherUser
from app.models.Grades import Grades

from app.time import now_semaster, now_year

from . import teacher

# 授课信息查询
@teacher.route('/query/course/arrange')
@login_required
@teacher_required
def query_course_arrange():
    gtoi = {
        u"一": 1,
        u"二": 2,
        u"三": 3,
        u"四": 4,
        u"五": 5,
        u"六": 6,
        u"七": 7,
    }
    courses = current_user.get_teacher().arranges.all()
    schedule = [ ['' for g in range(12)] for x in range(8) ]
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
        'teacher/course_schedule.html',
        schedule=schedule
    )

# 点名册查询
@teacher.route('/query/course/student/list')
@login_required
@teacher_required
def query_course_student_list():
    arranges = []
    for arrange in current_user.get_teacher().arranges.all():
        # 去除不是本学期的课程
        if arrange.year != now_year() or arrange.semaster != now_semaster():
            continue
        arranges.append(arrange)

    return render_template(
        'teacher/course_student_list_index.html',
        arranges=arranges
    )

@teacher.route('/query/course/stduent/<int:id>')
@login_required
@teacher_required
def query_course_student(id):
    arrange = Arrange.query.filter_by(id=id).first()
    if arrange.teacher_id != current_user.id:
        return abort(403)
    students = []
    for s in arrange.student:
        students.append((User.query.filter_by(id=s.id).first().username, s))
    return render_template(
        'teacher/course_student_list.html',
        students=students,
        course_name=arrange.course.name
    )

# 教学班成绩查询
@teacher.route('/query/course/grade')
@login_required
@teacher_required
def query_course_grade_list():
    arranges = []
    for arrange in current_user.get_teacher().arranges.all():
        # 去除不是本学期的课程
        if arrange.year != now_year() or arrange.semaster != now_semaster():
            continue
        arranges.append(arrange)

    return render_template(
        'teacher/query_course_grade_index.html',
        arranges=arranges
    )

@teacher.route('/query/course/grade/<int:id>')
@login_required
@teacher_required
def query_course_grade(id):
    arrange = Arrange.query.filter_by(id=id).first()
    if arrange.teacher_id != current_user.id:
        return abort(403)
    students = []
    for s in arrange.student:
        score = Grades.query.filter_by(arrange_id=arrange.id, student_id=s.id).first()
        if score is None or score.grade is None:
            score = ''
        else:
            score = score.grade
        students.append((User.query.filter_by(id=s.id).first().username, s, score))
    return render_template(
        'teacher/query_course_grade.html',
        arrange_id=arrange.id,
        students=students,
        course_name=arrange.course.name
    )


# 成绩录入
@teacher.route('/input/course/grade')
@login_required
@teacher_required
def input_course_grade_list():
    arranges = []
    for arrange in current_user.get_teacher().arranges.all():
        # 去除不是本学期的课程
        if arrange.year != now_year() or arrange.semaster != now_semaster():
            continue
        arranges.append(arrange)

    return render_template(
        'teacher/input_course_grade_index.html',
        arranges=arranges
    )

@teacher.route('/input/course/grade/<int:id>', methods=['GET', 'POST'])
@login_required
@teacher_required
def input_course_grade(id):
    arrange = Arrange.query.filter_by(id=id).first()
    if arrange.teacher_id != current_user.id:
        return abort(403)
    students = []
    for s in arrange.student:
        score = Grades.query.filter_by(arrange_id=arrange.id, student_id=s.id).first()
        if score is None or score.grade is None:
            score = ''
        else:
            score = score.grade
        students.append((User.query.filter_by(id=s.id).first().username, s, score))
    return render_template(
        'teacher/input_course_grade.html',
        arrange_id=arrange.id,
        students=students,
        course_name=arrange.course.name
    )

@teacher.route('/input/course/grade/<int:sid>/<int:aid>/', methods=['GET', 'POST'])
@login_required
@teacher_required
def add_grade(aid, sid):
    score = Grades.query.filter_by(arrange_id=aid, student_id=sid).first()
    rgrade = request.args.get('grade')
    if score is None:
        score = Grades(
            arrange_id=aid,
            student_id=sid,
            grade=rgrade
        )
    else:
        score.grade = rgrade

    db.session.add(score)
    db.session.commit()
    return redirect(url_for('teacher.input_course_grade', id=aid))

