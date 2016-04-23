# -*- coding: utf-8 -*-
#coding=utf-8

from . import Role, User
from Role import Role
from User import add_administrator_user
from TimeSpan import TimeSpan

def init_models():
    Role.create_base_role()
    add_administrator_user()
    TimeSpan.add_default_timespan()
