#encoding=utf-8
import os
import uuid
from flask import render_template,redirect,url_for,abort,session,request,flash,get_flashed_messages, send_from_directory
import logging
from models import User,Image,Comment
from picture_share import app,db
from flask_login import login_user,login_required,logout_user,current_user
import qiniuSDK

import  random,json
import hashlib

@app.route("/")
def index():
    try:
        images = Image.query.order_by(Image.id.desc()).limit(3).all()
        paginate = Image.query.order_by(db.desc(Image.id)).paginate(page=1, per_page=4, error_out=False)
        map = {'has_next': paginate.has_next}
        images = []
        for image in paginate.items:
            comments = []
            for i in range(0, min(2, len(image.comments))):
                comment = image.comments[i]
                comments.append({'username':comment.user.username,
                                 'user_id':comment.user_id,
                                 'content':comment.content})
            imgvo = {'image_id': image.id,
                     'image_url': image.url,
                     'user_id':image.user.id,
                     'user_name':image.user.username,
                     'user_avatar':image.user.avatar,
                     'comment_count': len(image.comments),
                     'create_date':str(image.create_date),
                     'comments':comments}
            images.append(imgvo)

        map['images'] = images
        return render_template("index.html",imagevos=map)
    except (Exception) as e:
        print e
        return render_template('error_404.html')

@app.route("/image/<int:image_id>/")
def page_detail(image_id):
    image = Image.query.get(image_id)
    if image == None:
        return redirect("/")
    else:
        return render_template("pageDetail.html",image=image)

@app.route("/profile/<int:user_id>/")
@login_required # 表示当前页需要登录才能访问
def profile_page(user_id):
    user = User.query.get(user_id)
    if user == None:
        return redirect("/reglogin/")
    else:
        paginate = Image.query.filter_by(user_id=user.id).paginate(page=1,per_page=3)
        return render_template("profile.html",user=user,images=paginate.items,has_next=paginate.has_next,page=1,pageSize=2)

@app.errorhandler(404)
def page_not_found(error):
    return render_template("error_404.html"),404


def redirect_with_msg(url,msg,category):
    if msg!=None:
        flash(msg,category=category)
    return redirect(url)

@app.route('/reg/',methods={'post','get'})
def reg():
    username = request.values.get('username').strip()
    password = request.values.get('password').strip()
    if username == None or password==None:
        return redirect_with_msg('/reglogin',u'用户名密码不能为空','reglogin')
    user = User.query.filter_by(username = username).first()
    if user != None:
        return redirect_with_msg('/reglogin',u'用户名已经存在','reglogin')
    # more validation

    # insert user
    salt = '.'.join(random.sample('Absdfsk212397KLA*&!klfas',10))
    m = hashlib.md5()
    m.update(password+salt)
    password = m.hexdigest()

    user = User(username,password,salt)
    db.session.add(user)
    db.session.commit()
    return redirect_with_msg('/reglogin',u'注册成功','reglogin')

#login
@app.route('/reglogin/',methods={'post','get'})
def reglogin():

    if current_user.is_authenticated :
        return redirect('/')

    msg=''
    for m in get_flashed_messages(with_categories=False ,category_filter=['reglogin']):
        msg += m
    return render_template('login.html',msg = msg,next=request.values.get('next'))

@app.route('/login/',methods={'post'})
def login():
    username = request.values.get('username').strip()
    password = request.values.get('password').strip()

    if username == None or password == None:
        return redirect_with_msg('/reglogin',u'用户名密码不能为空','reglogin')

    user = User.query.filter_by(username=username).first()
    if user == None:
        return redirect_with_msg('/reglogin',u'用户名不存在','reglogin')

    m = hashlib.md5()
    m.update(password+user.salt)
    if m.hexdigest() != user.password:
        return redirect_with_msg('/reglogin',u'密码错误','reglogin')

    # login sucess!
    login_user(user)

    # 改变登录连，如果用户登录前是从别的页面被需要登录的规则拦截后跳过来的，当用户登录完成需要自动跳到用户本来要去的页面
    # 在跳转到登录页面之前会在url参数里面加了一个 next 参数，记录了 下一个 页面的地址
    next = request.values.get('next')
    app.logger.debug(next)
    if next != u'None':
        # 说明用户是从别的页面跳过来的
        return redirect(next)
    return redirect('/')

@app.route('/logout/',methods=['post','get'])
def logout():
    logout_user()
    return redirect('/')


# '/profile/images/' + oConf.uid + '/' + oConf.page + '/' + oConf.pageSize + '/';
@app.route('/profile/images/<int:uid>/<int:page>/<int:pagesize>/')
def paginate_image(uid,page,pagesize):
    paginate = Image.query.filter_by(user_id=uid).paginate(page=page,per_page=pagesize)
    res = {'has_next':paginate.has_next}
    images = []
    for image in paginate.items:
        imginfo = {'id':image.id,'url':image.url,'comment_count':len(image.comments)}
        images.append(imginfo)
    res['images']=images
    return json.dumps(res)


def save_to_local(file,file_name):
    save_dir = app.config['UPLOAD_DIR']
    path = os.path.join(save_dir,file_name)
    file.save(path)
    return '/image/'+file_name

@app.route('/image/<image_name>')
def view_image(image_name):
    return send_from_directory(app.config["UPLOAD_DIR"],image_name)


@app.route('/upload/',methods={'post','get'})
def upload():
    print type(request.files)
    file = request.files['file']
    # 判断文件名是否正确
    file_ext = ''
    if file.filename.find('.')>0:
        file_ext = file.filename.rsplit('.',1)[1].strip().lower()
    if file_ext in app.config['ALLOWED_EXT']:
        file_name = str(uuid.uuid1()).replace('-','')+'.'+file_ext
        # url = save_to_local(file,file_name)
        url = qiniuSDK.qiniu_upload_file(file,file_name)
        if url is not None:
            db.session.add(Image(url,current_user.id))
            db.session.commit()
    return redirect('/profile/%d' % current_user.id)

@app.route('/addcomment/',methods={'post'})
def add_comment():
    is_login = current_user.is_authenticated
    image_id = int(request.values['image_id'])
    content = request.values['content'].strip()
    user_id = current_user.id if is_login==True else 1
    comment = Comment(content,user_id,image_id)
    db.session.add(comment)
    db.session.commit()
    return json.dumps({"code":0,"id":comment.id,"content":content,"username":comment.user.username})


@app.route('/images/<int:page>/<int:per_page>/',methods={'get'})
def index_images(page, per_page):
    paginate = Image.query.order_by(db.desc(Image.id)).paginate(page=page, per_page=per_page, error_out=False)
    map = {'has_next': paginate.has_next}
    images = []
    for image in paginate.items:
        comments = []
        for i in range(0, min(2, len(image.comments))):
            comment = image.comments[i]
            comments.append({'username':comment.user.username,
                             'user_id':comment.user_id,
                             'content':comment.content})
        imgvo = {'image_id': image.id,
                 'image_url': image.url,
                 'username':image.user.username,
                 'comment_count': min(2,len(image.comments)),
                 'user_id': image.user_id,
                 'head_url':image.user.avatar,
                 'create_date':str(image.create_date),
                 'comments':comments}
        images.append(imgvo)

    map['images'] = images
    return json.dumps(map)

