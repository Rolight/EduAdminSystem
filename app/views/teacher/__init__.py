# -*- coding: utf-8 -*-
#coding=utf-8

from flask import Blueprint

teacher = Blueprint('teacher', __name__)

from . import views