# -*- coding: utf-8 -*-
#coding=utf-8


# 分数转化为GPA
def grade_to_GPA(grade):
    if grade >= 90:
        return 4.0
    elif 85 <= grade <= 89:
        return 3.6
    elif 80 <= grade <= 84:
        return 3.2
    elif 75 <= grade <= 79:
        return 2.8
    elif 70 <= grade <= 74:
        return 2.3
    elif 65 <= grade <= 69:
        return 1.8
    elif 60 <= grade <= 64:
        return 1.0
    else:
        return 0.0