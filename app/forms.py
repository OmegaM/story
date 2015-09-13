#!/usr/bin/env python
# -*- coding:utf-8 -*-


"""Created with Pycharm IDEA

@Create on 2015/9/12 16:31

@my_story forms.py

@author : OmegaMiao"""

from models import Category
from flask_wtf import Form

from wtforms import TextAreaField, StringField
from wtforms.validators import DataRequired, Length
from wtforms.ext.sqlalchemy.fields import QuerySelectField


# def category_selector():
#     category_dict = {}
#     for obj in db.session.query(Category).all():
#         category_dict[obj.id] = obj.name
#     return category_dict.items()
class StoryForm(Form):
    title = StringField(label='Title', validators=[DataRequired(message=u"该字段为必填项"),
                                                   Length(min=1, max=30, message=u"大于500")])
    content = TextAreaField(label='Content', validators=[DataRequired(u"该字段为必填项"), Length(min=1, max=500)])
    author = StringField(label='Author', validators=[DataRequired(u"该字段为必填项")])
    nick_name = StringField(label='Nick Name', validators=[DataRequired(u"该字段为必填项")])
    # category = SelectField(label='Category', choices=category_selector(), coerce=int)
    category = QuerySelectField(label='Category', query_factory=Category.query.all,
                                get_pk=lambda a: a.id, get_label=lambda a: a.name)
