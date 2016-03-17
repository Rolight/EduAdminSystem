# -*- coding: utf-8 -*-
#coding=utf-8
from flask import render_template, redirect, request, url_for, flash
from flask.ext.login import login_user
from flask.ext.login import logout_user, login_required
from . import auth
from ..models import User
from .forms import LoginForm

@auth.route('/login', methods = ['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is not None and user.verify_password(form.password.data):
            login_user(user, form.remember_me.data)
            return redirect(request.args.get('next') or url_for('main.index'))
        flash(u'不正确的用户名或者密码!')
    return render_template('auth/login.html', form=form)

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash('您现在已经登出')
    return redirect(url_for('main.index'))



