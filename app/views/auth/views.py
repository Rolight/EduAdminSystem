# -*- coding: utf-8 -*-
#coding=utf-8
from flask import render_template, redirect, request, url_for, flash
from flask_login import login_user
from flask_login import logout_user, login_required
from . import auth
from app.models.User import StudentUser, User, TeacherUser, DepartmentUser
from app import db
from .forms import LoginForm, RegistrationForm, StudentInformationForm

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

@auth.route('/register/student', methods=['GET', 'POST'])
def register_student():
    form = StudentInformationForm()

    if form.validate_username() and form.validate_major() and form.validate_class():
        stu = StudentUser(
            username=form.username.data,
            password=form.password.data,
            name=form.name.data,
            sex=form.sex.data,
            nation=form.nation.data,
            public=form.public.data,
            idcard=form.idcard.data,
        )
    return ''

