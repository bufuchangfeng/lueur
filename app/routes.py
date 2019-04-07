# -*- coding:utf-8 -*-
from app import app, db
from flask import render_template, request, redirect, url_for, jsonify
from app.models import Category, Post, Admin
from flask_login import login_required, login_user, logout_user
from app.forms import LoginForm, PostForm
from datetime import datetime
import json


@app.route('/')
def index():
    return render_template("index.html")


@app.route('/new_post', methods=['GET', 'POST'])
@login_required
def new_post():
    form = PostForm()
    if form.validate_on_submit():
        title = form.title.data
        body = form.body.data
        category = db.session.query(Category).filter_by(name=form.category.data).first()
        post = Post(title=title, body=body, category=category, timestamp=datetime.now())

        db.session.add(post)
        db.session.commit()

        return redirect(url_for('.show_post', post_id=post.id))
    return render_template('/admin/new_post.html', form=form)


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/category', methods=['GET', 'POST'])
@app.route('/category/<int:category_id>', methods=['GET', 'POST'])
def show_posts(category_id=0):
    page = request.args.get('page', 1, type=int)
    if 0 != category_id:
        category = Category.query.get_or_404(category_id)
        pagination = Post.query.with_parent(category).order_by(Post.id.asc()).paginate(page, per_page=5)
    else:
        pagination = Post.query.order_by(Post.id.asc()).paginate(page, per_page=5)
    posts = pagination.items
    categories = Category.query.all()
    return render_template('posts.html', posts=posts, pagination=pagination, categories=categories)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        admin = Admin.query.first()
        if admin is not None and admin.verify_password(form.password.data):
            login_user(admin)
            return redirect(request.args.get('next') or url_for('index'))
    return render_template('/admin/login.html', form=form)


@app.route('/post/<int:post_id>', methods=['GET', 'POST'])
def show_post(post_id):
    post = Post.query.get_or_404(post_id)
    return render_template("post.html", post=post)


@app.route('/post/<int:post_id>/delete', methods=['GET', 'POST'])
@login_required
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    db.session.delete(post)
    db.session.commit()
    return redirect(url_for('manage'))


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/manage')
@login_required
def manage():
    posts = Post.query.order_by(Post.id.asc())
    categories = Category.query.order_by(Category.id.asc())
    return render_template("/admin/manage.html", posts=posts, categories=categories)


@app.route('/edit/<int:post_id>', methods=['GET', 'POST'])
@login_required
def edit_post(post_id):
    post = Post.query.get_or_404(post_id)
    form = PostForm()
    if form.validate_on_submit():
        post.title = form.title.data
        post.body = form.body.data

        post.timestamp = datetime.now()

        post.category = db.session.query(Category).filter_by(name=form.category.data).first()

        db.session.commit()
        return redirect('/post/' + str(post.id))
    form.title.data = post.title
    form.body.data = post.body
    form.category.data = post.category.name
    return render_template('/admin/edit_post.html', form=form)


@app.route('/update_category', methods=['POST'])
@login_required
def udapte_category():
    if request.method == 'POST':
        data = json.loads(request.get_data())
        category_id = data['category_id']
        category_name = data['category_name']

        category = Category.query.get_or_404(category_id)
        category.name = category_name

        db.session.commit()

        return jsonify({"result": "success"})


@app.route('/new_category', methods=['POST'])
@login_required
def new_category():
    if request.method == 'POST':
        data = json.loads(request.get_data())
        category_name = data['category_name']

        category = Category(name=category_name)

        db.session.add(category)

        db.session.commit()

        return jsonify({"result": "success"})


@app.route('/delete_category', methods=['POST'])
@login_required
def delete_category():
    if request.method == 'POST':
        data = json.loads(request.get_data())
        category_id = data['category_id']

        category = Category.query.get_or_404(category_id)

        db.session.delete(category)
        db.session.commit()
        return jsonify({"result": "success"})
