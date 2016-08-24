#encoding=utf-8

from sqlalchemy import or_,and_

from flask_script import Manager
from picture_share import app
from picture_share import db
from picture_share.models import User,Image,Comment
import random as rd

manager = Manager(app)

def get_url():
    #return "http://imglf1.nosdn.127.net/img/Z0hpMWtqYzRpVVhheW9mYXhJU0ZRWWhYY00zdzdYdVRBcXEwWnVENmR6bnpYWjlaZHhtU0R3PT0.jpg?imageView&thumbnail=500x0&quality=96&stripmeta=0&type=jpg"
    return 'http://images.nowcoder.com/head/'+str(rd.randint(0,1000))+'m.png'

@manager.command
def init_database():
    db.drop_all()
    db.create_all()
    # add users
    for i in range(0,20):
        db.session.add(User('usr{0}'.format(i),'pwd','',"http://jinja.pocoo.org/docs/dev/_static/jinja-small.png"))
        for j in range(0,10): # user - image is one 2 many relation
            db.session.add(Image(get_url(),i+1))
            for k in range(0,3):
                db.session.add(Comment('good {0}'.format((i+1)*10),i+1,i*10+j+1))
    db.session.commit()

@manager.command
def query():
    print User.query.get(1)
    print User.query.all()
    print User.query.filter_by(id=1)
    print User.query.filter_by(id=1).all()
    print User.query.filter(User.id < 3).all()
    print User.query.filter(and_(User.username.startswith('u'),User.id < 4))
    print User.query.filter(and_(User.username.startswith('u'),User.id < 4)).all()
    print User.query.filter(and_(User.username.endswith('3'),User.id < 50)).all()
    print User.query.filter(or_(User.username.endswith('1'),User.username.endswith('2'))).all()
    print User.query.order_by(User.id.desc()).all()
    # pagenate
    print User.query.order_by(User.id.asc()).paginate(page=1,per_page=10).items

    print('--------------------------------------------------------------------------')
    # one to many
    a_user = User.query.get(1)
    for image in a_user.images:
        print image
        for comment in image.comments:
            print comment

    # many to one
    # 用backref来反向关联 ,dynamic来让它执行的时候再关联
    # 比如要查找image对应的user,直接 image.user是没有的，因为image这时候还没有user属性，
    image = Image.query.get(1)
    # 需要在 User的关系中设置 backref，image才能关联到 user
    print("image.user is : {0} ".format(image.user))


@manager.command
def update():
    # update function
    User.query.filter_by(id=1).update({'username':'anboqing','password':'pwd'})
    db.session.commit()
    # update by setting field
    user = User.query.get(1)
    user.username = 'anboqingqing'
    db.session.commit()

import unittest
@manager.command
def runtest():
    tests = unittest.TestLoader().discover("/")

if __name__ == "__main__":
    manager.run()
