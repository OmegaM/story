#!/usr/bin/env python
# -*- coding:utf-8 -*-


"""Created with Pycharm IDEA

@Create on 2015/9/13 19:41

@my_story test_story.py

@author : OmegaMiao"""


import unittest
import json
from app import app, db
from app.models import Story, Author, Category
from config import config


class StoryTestCase(unittest.TestCase):
    def setUp(self):
        app.config.from_object(config['dev'])
        app.config['TESTING'] = True
        self.app = app.test_client()

    def tearDown(self):
        pass

    def test_index(self):
        self.assertTrue("left" in self.app.get('/').data)

    def test_get_story_is_dict(self):
        self.assertTrue(isinstance(json.loads(self.app.get('/story/1').data), dict))

    def test_get_story(self):
        self.assertEqual(json.loads(self.app.get('/story/1').data)['Story']['title'], 'Perl')

    def test_show_storys(self):
        self.assertTrue("Tody is Sunday" in self.app.get('/show_storys').data)

    def test_add_story(self):

        # print "---------" + self.app.post('/add_story', data=dict(
        #     title='Test',
        #     content='Test',
        #     author='Test',
        #     nick_name='Test',
        #     category=Category.query.get(1)
        # ), follow_redirects=True).data
        self.assertTrue(self.app.post('/add_story', data=dict(
            title='Test',
            content='Test',
            author='Test',
            nick_name='Test',
            category=Category.query.get(1)
        ), follow_redirects=True).data is not None)
