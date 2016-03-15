# encoding=utf-8

import mysql.connector

def create_table(user, passwd, database_name):
    conn = mysql.connector.connect(host = 'localhost', user = user, passwd = passwd, database = database_name)
    cursor = conn.cursor()
    # create the table
    cursor.execute(r"""
    create table if not exists tuser(
        userID varchar(50),
        password char(32) not null,
        username varchar(20) not null,
        identity varchar(20) not null,
        sex char(2) not null,
        nation varchar(20),
        publicist varchar(20),
        idcard char(30),
        brithday date,
        enterday date,
        department varchar(20),
        major varchar(30),
        class varchar(30),
        primary key (userID),
        check (sex in ('男', '女')),
        check (identity in ('研究生', '本科生', '博士生', '教师', '院系用户'))
    );

    create table if not exists tclass (
        classID varchar(50),
        classNumber char(10) not null,
        classname varchar(50) not null,
        classkind char(20) not null,
        teacherID varchar(50) not null,
        credit float not null,
        timeepreweek int not null,
        spantime int not null,
        location varchar(30) not null,
        department varchar(30) not null,
        introduction varchar(50) not null,
        primary key (classID)
    );

    create table if not exists tsc (
        studentID varchar(50),
        classID varchar(50),
        times int,
        grade int,
        primary key (studentID, classID, times)
    );

    alter table tclass add foreign key (teacherID) references tuser(userID);
    alter table tsc add foreign key (classID) references tclass(classID);
    alter table tsc add foreign key (studentID) references tuser(userID);
    """, multi=True)
    cursor.close()

create_table('root', 'loulinhui', 'EduAdminSystem')

