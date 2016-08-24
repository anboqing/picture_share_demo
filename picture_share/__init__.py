#encoding=utf-8
import logging
from logging.handlers import RotatingFileHandler

from flask import Flask

from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.jinja_env.add_extension('jinja2.ext.loopcontrols')
app.config.from_pyfile('app.conf')

app.secret_key="mamailoveyouandmissyou"

db = SQLAlchemy(app)

from picture_share import views,models

def set_logger():
    info_file_handler = RotatingFileHandler('d:\\info.txt')
    info_file_handler.setLevel(logging.INFO)
    app.logger.addHandler(info_file_handler)

    warn_file_handler = RotatingFileHandler('d:\\warn.txt')
    warn_file_handler.setLevel(logging.WARN)
    app.logger.addHandler(warn_file_handler)

    error_file_handler = RotatingFileHandler('d:\\error.txt')
    error_file_handler.setLevel(logging.ERROR)
    app.logger.addHandler(error_file_handler)

set_logger()

# settting login information
from flask_login import LoginManager
# 关联app和loginmanager
login_manager = LoginManager()
login_manager.init_app(app)

# 注册callback
@login_manager.user_loader
def user_loader(user_id):
    return models.User.query.get(user_id)

login_manager.login_view = '/reglogin/'
