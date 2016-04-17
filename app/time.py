# -*- coding: utf-8 -*-
#coding=utf-8

from datetime import datetime

# 获取当前学年
def now_year():
    return datetime.now().year

# 获取当前学期
def now_semaster():
    if datetime.now().month < 7:
        return 1
    else:
        return 2
