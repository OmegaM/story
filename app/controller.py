#!/usr/bin/env python
# -*- coding:utf-8 -*-


"""Created with Pycharm IDEA

@Create on 2015/9/12 16:31

@my_story controllers.py

@author : OmegaMiao"""


from app import app
from flask import jsonify, request, render_template, redirect, flash, url_for
from models import Story
from forms import StoryForm
from service import StoryService


@app.route('/')
def index():
    form = StoryForm()
    return render_template('index.html', form=form)


@app.route('/story/<int:story_id>')
def get_story(story_id):
    return jsonify(StoryService.get_story(story_id))


# @app.route('/storys')
# def get_storys():
#     return jsonify(StoryService.get_storys())


@app.route('/show_storys', methods=['GET'])
def show_storys():
    page = request.args.get('page', 1, type=int)
    pagination = StoryService.get_storys(page)
    storys = pagination.items
    return render_template('story_detail.html', storys=storys, pagination=pagination)


@app.route('/delete_story/<int:story_id>')
def delete_story(story_id):
    return jsonify(StoryService.delete_story(story_id))


@app.route('/add_story', methods=['POST'])
def add_story():
    form = StoryForm(request.form)
    if request.method == 'POST' and form.validate_on_submit():

        story = Story(form.title.data, form.content.data)
        try:
            StoryService.add_story(story=story,
                                   nick_name=form.nick_name.data,
                                   category=form.category.data,
                                   author=form.author.data)
            flash("add success")
            return redirect(url_for('index'))
        except Exception, e:
            return jsonify({"errorMessage": e.message})
    return render_template('index.html', form=form)
