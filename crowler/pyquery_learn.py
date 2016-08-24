#encoding=utf-8

from pyquery import PyQuery

import datetime

if __name__ =="__main__":
    q = PyQuery(open("V2EX.html").read())


    #
    for each in q('div.inner>a').items():
        if each.attr.href.find('tab')>0:
            print 1,each.attr.href,each.html()


    # #id 是id选择器
    for each in q('#Tabs>a').items():
        print 2,each.attr.href

    # > 是紧邻的层级关系
    for each in q('.cell>a[href^="/go/"]').items():
        print 3,each.attr.href

    # 空格不必父子
    for each in q('.cell a[href^="/go/programmer"]').items():
        print 4,each.attr.href

    for each in q('div.cell.item span.item_title>a').items():
        print 5,each.html()

    print type(datetime.datetime.today())
    print datetime.datetime.strftime(datetime.datetime.today(),"%Y-%m-%d %H:%M:%S")