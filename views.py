from app import app
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from flask import Flask, request, redirect, url_for, render_template, session
from models import Tweets, User
from urlparse import urlparse, urljoin
from datetime import datetime
import itertools
import hashlib
from werkzeug.security import generate_password_hash, check_password_hash
from app import db

@app.route('/')
def root():
    return redirect(url_for('timeline'))

@app.route('/blog', methods=['GET'])
def blog():
    if request.method == 'GET':
        posts = Tweets.query.all()
        #uid = current_user.id
        #user = User.query.filter_by(id=uid).first()
        #posts = Tweets.query.filter().order_by(Tweets.id.desc()).all()        
        return render_template('blog.html', posts = posts)


@app.route('/blog/<int:id>', methods=['GET', 'DELETE'])
def show(id):
    tweet = Tweets.query.filter_by(id=id).first()
    if request.method == 'DELETE':
        db.session.delete(tweet)
        db.session.commit()
        return redirect(url_for('timeline'))

@app.route('/blog/create')
def create():
        return render_template('create.html')

@app.route('/twitter/login')
def login():
    #session['next'] = request.args.get('next')
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
    #if 'next' in session:
    #    next = session['next']
    #    if is_safe_url(next):
    return redirect(url_for('timeline'))

@app.route('/twitter/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('root'))

@app.route('/blog/register')
def registration():
    return render_template('register.html')

@app.route('/twitter/register', methods=['POST'])
def register():
    login = request.form['login']
    password = generate_password_hash(request.form['password'])
    nickname = request.form['nickname']
    u = User(username=login,password=password, nickname=nickname)
    db.session.add(u)
    db.session.commit()
    return redirect(url_for('login'))

def is_safe_url(target):
    ref_url = urlparse(request.host_url)
    test_url = urlparse(urljoin(request.host_url,target))
    return test_url.scheme in ('http','https') and \
        ref_url.netloc == test_url.netloc