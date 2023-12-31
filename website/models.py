from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    username = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(50))
    date_created = db.Column(db.DateTime(timezone=True), default=func.now())
    # -------------------------------------------------------------------------------------------------------------
    posts = db.relationship('Post', backref='usercha', passive_deletes=True)  #backref is important part!!!
    # Post sinfiga munosabat. Bu munosabat har bir foydalanuvchi ko'p postlarga ega bo'lishi mumkinligini anglatadi
    # -------------------------------------------------------------------------------------------------------------
    likes = db.relationship('Like', backref='likecha_user', passive_deletes=True)
class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String)  #learn
    text = db.Column(db.Text, nullable=False) #nullable mean is if input is empty
    # -------------------------------------------------------------------------------------------------------------
    author_id = db.Column(db.Integer(), db.ForeignKey('user.id', ondelete="CASCADE"), nullable=False) #please find more information for this line
    # Foydalanuvchi sinfining id maydoniga havola qiluvchi tashqi kalit. Bu shuni anglatadiki, har bir post bitta foydalanuvchi bilan bog'lanishi kerak
    # -------------------------------------------------------------------------------------------------------------
    date_created = db.Column(db.DateTime(timezone=True), default=func.now())
    comments = db.relationship('Comment', backref='comentcha', passive_deletes=True)
    likes = db.relationship('Like', backref='likecha', passive_deletes=True)

class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.Text, nullable=False)
    post_id = db.Column(db.Integer, db.ForeignKey('post.id', ondelete='CASCADE'), nullable=False)
    date_created = db.Column(db.DateTime(timezone=True), default=func.now())
    author = db.Column(db.String)


class Like(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    post_id = db.Column(db.Integer(), db.ForeignKey('post.id', ondelete='CASCADE'), nullable=False)
    author_id = db.Column(db.Integer(), db.ForeignKey('user.id', ondelete='CASCADE'), nullable=False)
    date_created = db.Column(db.DateTime(timezone=True), default=func.now())