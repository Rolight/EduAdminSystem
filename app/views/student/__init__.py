# -*- coding: utf-8 -*-
#coding=utf-8

from flask import Blueprint

student = Blueprint('student', __name__)

from . import views