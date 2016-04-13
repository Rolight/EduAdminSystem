# -*- coding: utf-8 -*-
#coding=utf-8
from datetime import datetime
from flask import render_template, session, redirect, url_for

from . import main
from .forms import NameForm
from app import db
from app.models import User

@main.route('/', methods=['GET', 'POST'])
def index():
    form = NameForm()
    if form.validate_on_submit():
        return redirect(url_for('.index'))

    return render_template('index.html', form=form, name=session.get('name'), know=session.get('known', False),
                           current_time=datetime.utcnow())

