#!/usr/bin/env python
# -*- coding:utf-8 -*-


"""Created with Pycharm IDEA

@Create on 2015/9/12 16:31

@my_story forms.py

@author : OmegaMiao"""

from models import Category
from flask_wtf import Form
from app.models import User, Author

from wtforms import TextAreaField, StringField, PasswordField, BooleanField, ValidationError
from wtforms.validators import DataRequired, Length, Email, Regexp, EqualTo
from wtforms.ext.sqlalchemy.fields import QuerySelectField


# def category_selector():
#     category_dict = {}
#     for obj in db.session.query(Category).all():
#         category_dict[obj.id] = obj.name
#     return category_dict.items()


class StoryForm(Form):
    title = StringField(label='Title', validators=[DataRequired(message=u"该字段为必填项"),
                                                   Length(min=1, max=30, message=u"大于30个字")])
    content = TextAreaField(label='Content', validators=[DataRequired(u"该字段为必填项"), Length(min=1, max=500)])
    author = StringField(label='Author', validators=[DataRequired(u"该字段为必填项")])
    nick_name = StringField(label='Nick Name', validators=[DataRequired(u"该字段为必填项")])
    # category = SelectField(label='Category', choices=category_selector(), coerce=int)
    category = QuerySelectField(label='Category', query_factory=Category.query.all,
                                get_pk=lambda a: a.id, get_label=lambda a: a.name)


class LoginForm(Form):
    email = StringField(label='Email', validators=[DataRequired(message=u'该字段为必填项'),
                                                   Length(min=1, max=64, message=u"输入的字符大于64个"),
                                                   Email(message=u"输入的邮箱地址不合法")])

    password = PasswordField(label='Password', validators=[DataRequired(message=u'该字段为必填项')])

    remember_me = BooleanField(label='Keep me logged in')


class RegistrationForm(Form):
    email = StringField(label='Email', validators=[DataRequired(message=u'该字段为必填项'),
                                                   Length(min=1, max=64, message=u"输入的字符大于64个"),
                                                   Email(message=u"输入的邮箱地址不合法")])

    username = StringField(label='Username', validators=[DataRequired(message=u'该字段为必填项'),
                                                         Length(min=1, max=64, message=u"输入的字符大于64个"),
                                                         Regexp('^[A-Za-z][A-Za-z0-9_.]*$', 0,
                                                                message=u'用户名仅支持英文，数字和下划线')])

    password = PasswordField(label='Password', validators=[DataRequired(message=u'该字段为必填项'),
                                                           EqualTo('password2', message=u'两次输入的密码必须匹配')])

    password2 = PasswordField(label='Confirm password', validators=[DataRequired(message=u'该字段为必填项')])

    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError(u'用户名邮箱已经被注册')

    def validate_username(self, field):
        if User.query.filter_by(username=field.data).first() or Author.query.filter_by(nick_name=field.data).first():
            raise ValidationError(u'用户名已经被占用')
