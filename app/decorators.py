# -*- coding: utf-8 -*-
#coding=utf-8

# 这个文件包含了所有关于用户权限的判定修饰器

from functools import wraps
from flask import abort
from flask_login import current_user
from app.models.Role import Permission

def permission_required(permission):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not current_user.can(permission):
                abort(403)
            return f(*args, **kwargs)
        return decorated_function
    return decorator

def admin_required(f):
    return permission_required(Permission.ADMIN)(f)

def student_required(f):
    return permission_required(Permission.STUDENT)(f)

def teacher_required(f):
    return permission_required(Permission.TEACHER)(f)

def department_required(f):
    return department_required(Permission.DEPARTMENT)(f)
