#!/usr/bin/env python
# -*- coding:utf-8 -*-


"""Created with Pycharm IDEA

@Create on 2015/9/12 17:12

@my_story service.py

@author : OmegaMiao"""


from app import db, app
from models import Story, Category, Author
from sqlalchemy.orm import joinedload
from sqlalchemy.orm.exc import NoResultFound
PER_PAGE = 2


class StoryService(object):

    def __init__(self):
        pass

    @staticmethod
    def get_story(_story_id):
        try:
            app.logger.debug("invoke get_story method...")
            result = db.session.query(
                Story.title,
                Story.create_time,
                Category.name,
                Author.nick_name,
                Story.content). \
                filter(Story.category_id == Category.id). \
                filter(Story.author_id == Author.id). \
                filter(Story.id == _story_id)

            return {"Story": {
                "title": result[0][0],
                "createtime": result[0][1].strftime('%Y-%m-%d %H:%M:%S'),
                "category": result[0][2],
                "author": result[0][3],
                "content": result[0][4]
            }}
        except Exception, e:
            app.logger.error(e.message)
            return {"errorMessage": e.message}
        finally:
            db.session.close()

    @staticmethod
    def get_storys(_page):
        # story_list = []
        try:
            pagination = Story.query.order_by(Story.create_time.desc()).options(joinedload('*')).\
                paginate(_page, PER_PAGE, error_out=False)
            # for i in results:
            #     story_list.append(i.to_json())
            return pagination
        except Exception, e:
            app.logger.error(e.message)
            return {"errorMessage": e.message}
        finally:
            db.session.close()

    @staticmethod
    def add_story(_story, _nick_name, _category, _author):
        print _author
        print _category  # this category is object!!!!!!
        if Author.query.filter(Author.nick_name == nick_name).count() >= 1:
            author = Author.query.filter(Author.nick_name == nick_name).all()[0]
        else:
            author = Author(_author, _nick_name)
        category = Category.query.get(_category.id)
        _story.author = author
        _story.category = category
        try:
            db.session.add(_story)
            db.session.commit()
        except Exception, e:
            app.logger.error(e.message)
            db.session.rollback()
        finally:
            db.session.close()

    @staticmethod
    def delete_story(_story_id):
        try:
            story = Story.query.get(_story_id)
            db.session.delete(story)
            db.session.commit()
            return {"message": "delete success!"}
        except Exception, e:
            app.logger.error(e.message)
            db.session.rollback()
        finally:
            db.session.close()

    @staticmethod
    def get_storys_by_author(_nick_name):
        author_story_list = []
        try:
            author = Author.query.filter(Author.nick_name == _nick_name).one()
            storys = author.storys
            for story in storys:
                author_story_list.append(story)
            return author_story_list
        except NoResultFound, e:
            app.logger.error(e.message)
            db.session.rollback()
        finally:
            db.session.close()

    @staticmethod
    def get_storys_by_category(_category_name):
        category_story_list = []
        try:
            category = Category.query.filter(Category.name == _category_name).one()
            storys = category.storys
            for story in storys:
                category_story_list.append(story)
            return category_story_list
        except NoResultFound, e:
            app.logger.error(e.message)
            db.session.rollback()
        finally:
            db.session.close()
