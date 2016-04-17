# -*- coding: utf-8 -*-
#coding=utf-8
from datetime import datetime
from flask import render_template, session, redirect, url_for

from . import main
from .forms import NameForm
from app import db
from app.models.Post import Post

# todo:在文章过多的时候分页
# todo:支持使用简单的MarkDown编辑器
@main.route('/', methods=['GET', 'POST'])
def index():
    posts = Post.query.order_by(Post.post_time.desc()).all()
    return render_template('main/index.html', posts=posts)

