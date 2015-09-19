#!/usr/bin/env python
# -*- coding:utf-8 -*-


"""Created with Pycharm IDEA

@Create on 2015/9/12 16:31

@my_story controllers.py

@author : OmegaMiao"""

from app import app
from flask import jsonify, request, render_template, redirect, flash, url_for
from flask.ext.login import login_required, login_user, logout_user
from models import Story, User
from forms import StoryForm, LoginForm
from service import StoryService


@app.route('/')
@login_required
def index():
    form = StoryForm()
    return render_template('index.html', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is not None and user.verify_password(form.password.data):
            login_user(user, form.remember_me.data)
            return redirect(request.args.get('next') or url_for('index'))
        flash(u'用户名或密码不正确')

    return render_template('login.html', form=form)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash(u'你已经登出')
    return redirect(url_for('index'))


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


@app.route('/story/<string:author_nickname>')
def get_story_by_author(author_nickname):
    # TODO: complete this get_story_by_author method
    pass


@app.route('/story/<string:category>')
def get_story_by_category(category):
    # TODO: complete this get_story_by_category method
    pass
