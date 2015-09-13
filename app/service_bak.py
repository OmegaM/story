#!/usr/bin/env python
# -*- coding:utf-8 -*-


"""Created with Pycharm IDEA

@Create on 2015/9/12 17:12

@my_story service.py

@author : OmegaMiao"""


from app import db
from models import Story, Category, Author
from sqlalchemy.orm import joinedload


class StoryService(object):

    def __init__(self):
        pass

    @staticmethod
    def get_story(story_id):
        try:
            result = db.session.query(
                Story.title,
                Story.create_time,
                Category.name,
                Author.nick_name,
                Story.content). \
                filter(Story.category_id == Category.id). \
                filter(Story.author_id == Author.id). \
                filter(Story.id == story_id)

            return {"Story": {
                "title": result[0][0],
                "createtime": result[0][1].strftime('%Y-%m-%d %H:%M:%S'),
                "category": result[0][2],
                "author": result[0][3],
                "content": result[0][4]
            }}
        except Exception, e:
            return {"errorMessage": e.message}
        finally:
            db.session.close()

    @staticmethod
    def get_storys():
        story_list = []
        try:
            results = Story.query.order_by(Story.create_time.desc()).options(joinedload('*')).all()
            print results[0].author
            for i in results:
                story_list.append(i.to_json())
            return {"StoryList": results}
        except Exception, e:
            return {"errorMessage": e.message}
        finally:
            db.session.close()

    @staticmethod
    def add_story(story, nick_name, category, author):
        print author
        print type(category)  # this category is object!!!!!!
        if Author.query.filter(Author.nick_name == nick_name).count() >= 1:
            author = Author.query.filter(Author.nick_name == nick_name).all()[0]
        else:
            author = Author(author, nick_name)
        category = Category.query.get(category.id)
        story.author = author
        story.category = category
        try:
            db.session.add(story)
            db.session.commit()
        except Exception, e:
            db.session.rollback()
        finally:
            db.session.close()

    @staticmethod
    def delete_story(story_id):
        try:
            story = Story.query.get(story_id)
            db.session.delete(story)
            db.session.commit()
            return {"message": "delete success!"}
        except Exception, e:
            db.session.rollback()
        finally:
            db.session.close()
