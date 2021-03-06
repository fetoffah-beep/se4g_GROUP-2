from flaskblog import db, login_manager
from flask_login import UserMixin
from datetime import datetime

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(15), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=True)
    comments = db.relationship('Comment', backref='author', lazy=True)
    #image_file = db.Column(db.String(20), default='default.jpg')
    
    def __repr__(self):
        return f"User('{self.username}', '{self.email}')"

class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    #title = db.Column(db.String(100), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f"Comment('{self.content}', '{self.date_posted}')"

class Data(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    x = db.Column(db.Float, nullable=False)
    y = db.Column(db.Float, nullable=False)
    vm = db.Column(db.Float, nullable=False)
    n = db.Column(db.Float, nullable=False)
    Sr = db.Column(db.Float, nullable=False)
    Wv = db.Column(db.Float, nullable=False)
    Wi = db.Column(db.Float, nullable=False)
    Ppk = db.Column(db.Float, nullable=False)
    Wb = db.Column(db.Float, nullable=False)
    fb = db.Column(db.Float, nullable=False)
    Wa = db.Column(db.Float, nullable=False)
    fsw = db.Column(db.Float, nullable=False)

    def __repr__(self):
        return f"Data('{self.x}', '{self.y}')"