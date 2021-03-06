from app import app
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from flask import Flask, request, redirect, url_for, render_template, session
from models import Tweets, User
from datetime import datetime
import itertools
import hashlib
from werkzeug.security import generate_password_hash, check_password_hash
from app import db

@app.route('/')
def root():
    return redirect(url_for('blog'))

#CREATE
@app.route('/blog/create')
@login_required
def create():
        return render_template('create.html')

@app.route('/blog', methods=['POST', 'GET'])
def blog():
    if request.method == 'POST':
        title = request.form['title']
        content = request.form ['content']
        slug = title.replace(" ", "-")
        post = Tweets(title=title, content=content, slug=slug)
        db.session.add(post)
        db.session.commit()
        return redirect(url_for('blog'))
    if request.method == 'GET':
        posts = Tweets.query.all()      
        return render_template('blog.html', posts = posts)

@app.route('/blog/<string:slug>', methods=["GET", "POST"])
def show(slug):
    post = Tweets.query.filter_by(slug=slug).first()    
    if request.method == 'POST':
        post.title = request.form['title']
        post.content = request.form['content']
        title = request.form['title']
        slug = title.replace(" ", "-")
        post.slug = slug                
        db.session.add(post)
        db.session.commit()
        return render_template('show.html', post=post)    
    return render_template('show.html', post=post)

#DELETE
@app.route('/blog/<int:id>', methods=["GET"])
def d(id):
    post = Tweets.query.filter_by(id=id).first() 
    if request.method == 'GET':
        db.session.delete(post)
        db.session.commit()
        return redirect(url_for('blog'))

@app.route('/blog/<string:slug>/adminctrl')
@login_required
def edit(slug):
        post = Tweets.query.filter_by(slug=slug).first()
        return render_template('edit.html', post = post)

@app.route('/blog/login')
def login():
    return render_template('login.html')

@app.route('/logmein', methods=['POST'])
def logmein():
    login = request.form['login']
    u = User.query.filter_by(username=login).first()
    check = check_password_hash(u.password, request.form['password']) 
    if not u:
        return '<h1>User not found </h1>'
    elif not check: 
        return '<h1>Wrong password </h1>'

    login_user(u, remember=True)
    return redirect(url_for('blog'))

@app.route('/blog/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('blog'))

@app.route('/blog/register')
def registration():
    return render_template('register.html')

@app.route('/blog/register', methods=['POST'])
def register():
    login = request.form['login']
    password = generate_password_hash(request.form['password'])
    nickname = request.form['nickname']
    u = User(username=login,password=password, nickname=nickname)
    db.session.add(u)
    db.session.commit()
    return redirect(url_for('login'))