# -*- coding:utf-8 -*-

from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, TextAreaField
from wtforms.validators import DataRequired
from wtforms.ext.sqlalchemy.fields import QuerySelectField
from app.models import Category


class LoginForm(FlaskForm):
    username = StringField(label='Username', validators=[DataRequired()])
    password = PasswordField(label='Password', validators=[DataRequired()])
    submit = SubmitField(label='Login')


class PostForm(FlaskForm):

    def query_category():
        categories = Category.query.all()
        r = []
        for category in categories:
            r.append(category.name)

        return r

    def get_pk(obj):
        return obj

    title = StringField(label='Title')
    body = TextAreaField(label='Body')
    category = QuerySelectField(label='Choose Category', query_factory=query_category, get_pk=get_pk)
    submit = SubmitField(label='Publish')