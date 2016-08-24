#encoding=utf-8
__author__ = '_anboqing_'
# 用 requests 模拟登陆
import requests
from bs4 import BeautifulSoup

def moni_login():
    login_url = "http://127.0.0.1:8080/login"
    login_data = {'username':'aa','password':'aa','rememberme':False}
    session = requests.session()
    response =  session.post(url=login_url,data=login_data)

    print response.cookies['ticket']

    res = session.get('http://localhost:8080/')

    # print res.cookies['ticket']

    # soup = BeautifulSoup(res,'html.parser')

def login():
     login_url = "http://127.0.0.1:8080/login"
     login_data = {'username':'aa','password':'aa','rememberme':False}
     res = requests.post(login_url,login_data,allow_redirects=False)
     print res.cookies['ticket']
     print res.url



if __name__=='__main__':
    # moni_login()
    login()

