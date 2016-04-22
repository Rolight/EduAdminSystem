# -*- coding: utf-8 -*-
#coding=utf-8

from . import Role, User
from Role import Role

def init_models():
    Role.create_base_role()