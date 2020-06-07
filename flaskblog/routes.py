from flask import render_template, url_for, flash, redirect, request
from flaskblog import app, db, bcrypt
from flaskblog.forms import RegistrationForm, LoginForm, CommentForm
from flaskblog.models import User, Comment
from flask_login import login_user, current_user, logout_user, login_required
from flaskblog.contents import cont

atama = cont()

@app.route('/')
@app.route('/home')
def home():
    return render_template('home.html', posts=atama)

@app.route('/about')
def about():
    return render_template('about.html', title='About')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_pass = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_pass)
        db.session.add(user)
        db.session.commit()
        flash(f'Account created!', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)  #where the user login
            next_page = request.args.get('next') # return none if parameter exist
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash('Please check username and password.', 'danger')
    return render_template('login.html', title='Login', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home'))

@app.route('/map', methods=['GET', 'POST'])
@login_required
def map():
    posts = Comment.query.all()
    return render_template('map.html', title='Map', posts=posts)

@app.route('/map/comments', methods=['GET', 'POST'])
@login_required
def post_comment():
    form = CommentForm()
    if form.validate_on_submit():
        post = Comment(content=form.content.data, author=current_user)
        db.session.add(post)
        db.session.commit()
        flash('Comment has been posted', 'success') ## bootstrap
        return redirect(url_for('map'))
    return render_template('comment.html', title='Comments', form=form)