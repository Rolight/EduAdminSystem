# -*- coding: utf-8 -*-
#coding=utf-8

from flask import render_template, redirect, request, url_for, flash
from flask_login import login_required, current_user
from . import admin

from app.models.Department import Department
from app.models.Class import Class
from app.models.Major import Major
from app.models.Place import Place
from app.models.TimeSpan import TimeSpan
from app.decorators import admin_required, department_required
from app import db
from .forms import AddClassForm, AddDepartmentForm, AddMajorForm, AddPlaceForm, AddTimeSpanForm


# 添加院系页面
@admin.route('/department/add', methods=['GET', 'POST'])
@login_required
@admin_required
def add_department():
    form = AddDepartmentForm()
    if form.validate_on_submit():
        department = Department(name=form.name.data)
        db.session.add(department)
        db.session.commit()
        flash(u'添加成功')
        return redirect(url_for('admin.add_department'))
    return render_template(
        'admin/add_department.html',
        form=form,
        departments=Department.query.all()
    )

# 删除院系
@admin.route('/department/del/<int:id>', methods=['GET', 'POST'])
@login_required
@admin_required
def del_department(id):
    department = Department.query.filter_by(id=id).first()
    if department:
        db.session.delete(department)
        db.session.commit()
    return redirect(url_for('admin.add_department'))

# 添加班级
@admin.route('/class/add', methods=['GET', 'POST'])
@login_required
@department_required
def add_class():
    form = AddClassForm()
    form.set_choices()
    classes = []
    for rclass in Class.query.all():
        if rclass.major.department_id == current_user.get_department().department_id:
            classes.append(rclass)
    if form.validate_on_submit():
        rclass = Class(name=form.name.data, major_id=form.major_name.data)
        db.session.add(rclass)
        db.session.commit()
        flash(u'添加成功')
        return redirect(url_for('admin.add_class'))
    return render_template(
        'admin/add_class.html',
        form=form,
        classes=classes
    )

# 删除班级
@admin.route('/del/class/<int:id>', methods=['GET', 'POST'])
@login_required
@department_required
def del_class(id):
    rclass = Class.query.filter_by(id=id).first()
    if rclass:
        db.session.delete(rclass)
        db.session.commit()
    return redirect(url_for('admin.add_class'))

# 添加专业
@admin.route('/major/add', methods=['GET', 'POST'])
@login_required
@department_required
def add_major():
    form = AddMajorForm()
    form.set_choices()
    if form.validate_on_submit():
        major = Major(name=form.name.data, department_id=form.department_name.data)
        db.session.add(major)
        db.session.commit()
        flash(u'添加成功')
        return redirect(url_for(admin.add_major))
    return render_template(
        'admin/add_major.html',
        form=form,
        majors=Major.query.filter_by(department_id=current_user.get_department().department_id).all()
    )

# 删除专业
@admin.route('/major/del/<int:id>', methods=['GET'])
@login_required
@department_required
def del_major(id):
    major = Major.query.filter_by(id=id).first()
    if major:
        db.session.delete(major)
        db.session.commit()
    return redirect(url_for('admin.add_major'))

# 添加上课地点
@admin.route('/place/add', methods=['GET', 'POST'])
@login_required
@department_required
def add_place():
    form = AddPlaceForm()
    if form.validate_on_submit():
        place = Place(
            name=form.name.data
        )
        db.session.add(place)
        db.session.commit()
    return render_template(
        'admin/add_place.html',
        form=form,
        places=Place.query.all()
    )

# 删除上课地点
@admin.route('/place/del/<int:id>', methods=['GET'])
@login_required
@department_required
def del_place(id):
    place = Place.query.filter_by(id=id).first()
    if place:
        db.session.delete(place)
        db.session.commit()
    return redirect(
        url_for('admin.add_place')
    )

# 添加上课时间
@admin.route('/timespan/add', methods=['GET', 'POST'])
@login_required
@department_required
def add_timespan():
    form = AddTimeSpanForm()
    if form.validate_on_submit():
        timespan = TimeSpan(
            name=form.name.data
        )
        db.session.add(timespan)
        db.session.commit()
    return render_template(
        'admin/add_timespan.html',
        form=form,
        timespans=TimeSpan.query.all()
    )

# 删除上课时间
@admin.route('/timespan/del/<int:id>', methods=['GET'])
@login_required
@department_required
def del_timespan(id):
    timespan = TimeSpan.query.filter_by(id=id).first()
    if timespan:
        db.session.delete(timespan)
        db.session.commit()
    return redirect(
        url_for('admin.add_timespan')
    )
