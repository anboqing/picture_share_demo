#encoding=utf-8
from picture_share import db
from datetime import datetime
import random

class User(db.Model):
    id = db.Column(db.Integer,primary_key=True,autoincrement=True)
    username=db.Column(db.String(80),unique=True)
    password=db.Column(db.String(80))
    salt =db.Column(db.String(80))
    avatar = db.Column(db.String(512))
    # relationship
    images = db.relationship("Image",backref='user',lazy='dynamic')

    def __init__(self,name,pwd,salt='',head_url=''):
        self.username = name
        self.password = pwd
        self.salt = salt
        self.avatar =head_url

    def __repr__(self):
        return '<user %d :  %s >'%(self.id,self.username)

    @property
    def is_authenticated(self):
        return True

    @property
    def is_active(self):
        return True

    @property
    def is_anonymous(self):
        return True

    def get_id(self):
        return self.id

class Image(db.Model):
    id = db.Column(db.Integer,primary_key=True,autoincrement=True)
    url = db.Column(db.String(512))
    user_id = db.Column(db.Integer,db.ForeignKey('user.id'))
    create_date = db.Column(db.DateTime)
    comments = db.relationship("Comment")

    def __init__(self,url,user_id):
        self.url = url
        self.user_id = user_id
        self.create_date = datetime.now()

    def __repr__(self):
        return "<User : %d > <Image : %s>" % (self.user_id,self.url)


class Comment(db.Model):
    id = db.Column(db.Integer,primary_key=True,autoincrement=True)
    content = db.Column(db.String(1024))
    user_id = db.Column(db.Integer,db.ForeignKey('user.id'))
    image_id = db.Column(db.Integer,db.ForeignKey('image.id'))
    status = db.Column(db.Integer) # 0 normal 1 deleted
    create_time = db.Column(db.DateTime)

    user = db.relationship("User")

    def __init__(self,content,user_id,image_id):
        self.content=content
        self.user_id= user_id
        self.image_id = image_id
        self.status = 1
        self.create_time = datetime.now()

    def __repr__(self):
        return "<Comment : %s uid: %d imageid %d > "%(self.content,self.user_id,self.image_id)
