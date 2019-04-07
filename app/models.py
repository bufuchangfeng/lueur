# -*- coding:utf-8 -*-
from app import db, login_manager
from datetime import datetime
from werkzeug.security import check_password_hash, generate_password_hash


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255))
    body = db.Column(db.Text)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

    like = db.Column(db.Integer, default=0)

    # foreign key
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'))

    # Category.posts
    category_post = db.relationship('Category', backref='posts')


class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text)

    # Post.category
    post_category = db.relationship('Post', backref='category')


class Admin(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(255))
    password_hash = db.Column(db.String(128))
    email = db.Column(db.String(255))

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    @property
    def is_authenticated(self):
        return True

    @property
    def is_active(self):
        return True

    @property
    def is_anonymous(self):
        return False

    def get_id(self):
        return str(self.id)


@login_manager.user_loader
def load_user(user_id):
    user = Admin.query.get(int(user_id))
    return user
