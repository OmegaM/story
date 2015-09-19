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
from app.service import StoryService
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

    def test_get_story_by_author(self):
        self.assertEqual(Author.query.filter(Author.nick_name == 'Steven Gerrard').one().storys[0].title, 'Perl')

    def test_get_story_list_by_author(self):
        self.assertTrue(len(StoryService.get_storys_by_author('Steven Gerrard')) == 2)

    def test_get_story_list_by_category(self):
        self.assertTrue(len(StoryService.get_storys_by_category('Java')) == 2)
