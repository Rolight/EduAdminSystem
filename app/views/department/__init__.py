# -*- coding: utf-8 -*-
#coding=utf-8

from flask import Blueprint

department = Blueprint('department', __name__)

from . import views