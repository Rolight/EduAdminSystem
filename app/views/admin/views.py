# -*- coding: utf-8 -*-
#coding=utf-8

from flask import render_template, redirect, request, url_for, flash
from flask_login import login_required
from . import admin

from app.models.Department import Department
from app.models.Class import Class
from app.models.Major import Major
from app.decorators import admin_required, department_required
from app import db
from .forms import AddClassForm, AddDepartmentForm, AddMajorForm


# 添加院系页面
@admin.route('/add/department', methods=['GET', 'POST'])
@login_required
@admin_required
def add_department():
    form = AddDepartmentForm()
    if form.validate_on_submit():
        department = Department(name=form.name.data)
        db.session.add(department)
        db.session.commit()
        flash(u'添加成功')
        return redirect(request.args.get('next') or url_for('main.index'))
    return render_template('admin/add_department.html', form=form)

@admin.route('/add/class', methods=['GET', 'POST'])
@login_required
@department_required
def add_class():
    form = AddClassForm()
    form.set_choices()
    if form.validate_on_submit():
        rclass = Class(name=form.name.data, major_id=form.major_name.data)
        db.session.add(rclass)
        db.session.commit()
        flash(u'添加成功')
        return redirect(request.args.get('next') or url_for('main.index'))
    return render_template('admin/add_class.html', form=form)

@admin.route('/add/major', methods=['GET', 'POST'])
@login_required
@admin_required
def add_major():
    form = AddMajorForm()
    form.set_choices()
    if form.validate_on_submit():
        major = Major(name=form.name.data, department_id=form.department_name.data)
        db.session.add(major)
        db.session.commit()
        flash(u'添加成功')
        return redirect(request.args.get('next') or url_for('main.index'))
    return render_template('admin/add_major.html', form=form)


