# -*- coding: utf-8 -*-
#coding=utf-8
from flask import render_template, redirect, request, url_for, flash
from flask_login import login_user
from flask_login import logout_user, login_required
from . import auth
from app.models.Role import Role
from app.models.User import StudentUser, User, TeacherUser, DepartmentUser
from app import db
from .forms import LoginForm, RegistrationForm, StudentUserInformationForm,\
    TeacherUserInformationForm, DepartmentUserInformationForm

# 登录
@auth.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is not None and user.verify_password(form.password.data):
            login_user(user, form.remember_me.data)
            return redirect(request.args.get('next') or url_for('main.index'))
        flash(u'不正确的用户名或者密码!')
    return render_template('auth/login.html', form=form)

# 登出
@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash(u'您现在已经登出')
    return redirect(url_for('main.index'))

# 注册学生用户
@auth.route('/register/student', methods=['GET', 'POST'])
def register_student():
    form = StudentUserInformationForm()
    form.set_chioces()

    if form.validate_on_submit():
        stu = StudentUser(
            role=Role.query.filter_by(name=u'Student').first(),
            username=form.username.data,
            password=form.password.data,
            name=form.name.data,
            sex=form.sex.data,
            nation=form.nation.data,
            public=form.public.data,
            idcard=form.idcard.data,
            birthday=form.birthday.data,
            in_time=form.in_time.data,
            degree=form.degree.data,
            department_id=form.department.data,
            major_id=form.major.data,
            class_id=form.rclass.data
        )
        db.session.add(stu)
        db.session.commit()
        flash(u'您已成功注册用户，现在将跳转到登录页面')
        return redirect(url_for('auth.login'))
    return render_template('auth/register_student.html', form=form)

# 注册教师用户
@auth.route('/register/teacher', methods=['GET', 'POST'])
def register_teacher():
    form = TeacherUserInformationForm()
    form.set_chioces()
    if form.validate_on_submit():
        teacher = TeacherUser(
            role=Role.query.filter_by(name=u'Teacher').first(),
            username=form.username.data,
            password=form.password.data,
            name=form.name.data,
            sex=form.sex.data,
            nation=form.nation.data,
            public=form.public.data,
            idcard=form.idcard.data,
            birthday=form.birthday.data,
            in_time=form.in_time.data,
            degree=form.degree.data,
            department_id=form.department.data,
        )
        db.session.add(teacher)
        db.session.commit()
        flash(u'您已成功注册用户，现在将跳转到登录页面')
        return redirect(url_for('auth.login'))
    return render_template('auth/register_teacher.html', form=form)

# 注册院系用户
@auth.route('/register/department', methods=['GET', 'POST'])
def register_department():
    form = DepartmentUserInformationForm()
    form.set_choices()

    if form.validate_on_submit():
        duser = DepartmentUser(
            role=Role.query.filter_by(name=u'Department').first(),
            username=form.username.data,
            password=form.password.data,
            department_id=form.department.data
        )
        db.session.add(duser)
        db.session.commit()
        flash(u'您已成功注册用户，现在将跳转到登录页面')
        return redirect(url_for('auth.login'))
    return render_template('auth/register_department.html', form=form)
