# -*- coding = utf-8 -*-
# @Time : 2021/12/1 11:20
# @Author : wjj
# @File : app.py
# @Software : PyCharm

import jieba
from matplotlib import pyplot as plt
from wordcloud import WordCloud
from PIL import Image
import numpy as np
import sqlite3
from flask import Flask,render_template,request
import pymysql


app = Flask(__name__)



@app.route('/')
def index():
    #数据量
    conn = pymysql.connect(
        host='127.0.0.1',
        user='root',
        password='root',
        port=3306,
        charset='utf8',
        db='boss'
    )  # 链接数据库
    cur = conn.cursor()
    sql = "select CAST(SUM(table_rows) as CHAR) from information_schema.tables where TABLE_SCHEMA = 'boss' order by table_rows;"
    cur.execute(sql)
    num = cur.fetchall()
    nums = []
    for datas in num:
        nums.append(datas[0])
    cur.close()
    conn.close()

    #岗位数量
    conn = pymysql.connect(
        host='127.0.0.1',
        user='root',
        password='root',
        port=3306,
        charset='utf8',
        db='boss'
    )  # 链接数据库
    cur = conn.cursor()
    sql = "SELECT COUNT(*) TABLES, table_schema FROM information_schema.TABLES   WHERE table_schema = 'boss';"
    cur.execute(sql)
    num1 = cur.fetchall()
    num = []
    for data in num1:
        num.append(data[0])
    cur.close()
    conn.close()
    #查询所有岗位
    conn = pymysql.connect(
        host='127.0.0.1',
        user='root',
        password='root',
        port=3306,
        charset='utf8',
        db='boss',
    )  # 链接数据库
    cur = conn.cursor()
    sql = 'SHOW TABLES FROM boss'
    cur.execute(sql)
    data = cur.fetchall()
    name = []
    for datas in data:
        name.append(datas[0])
    name = '  '.join(name)
    cur.close()
    conn.close()
    return render_template("index.html",num = nums,num1=num,name = name)


@app.route('/index')
def home():
    return index()

@app.route('/table1')
def data():
    kw = 'python'
    # if len(kw)==0:
    # kw = "python"
    #所有数据
    conn = pymysql.connect(
        host='127.0.0.1',
        user='root',
        password='root',
        port=3306,
        charset='utf8',
        db='boss'
    )  # 链接数据库
    cur = conn.cursor()
    sql = 'select * from `%s`'%(kw)
    cur.execute(sql)
    item = cur.fetchall()
    cur.close()
    conn.close()

    #最低工资
    conn = pymysql.connect(
        host='127.0.0.1',
        user='root',
        password='root',
        port=3306,
        charset='utf8',
        db='boss'
    )  # 链接数据库
    cur = conn.cursor()
    sql = "SELECT AVG(money1) FROM (SELECT SUBSTRING_INDEX(money,'-',1) as money1 FROM `%s`) as t1"%(kw)
    cur.execute(sql)
    lows = cur.fetchall()
    low = []
    for datas in lows:
        low.append(datas[0])
        low = list(map(int, low))
    cur.close()
    conn.close()
    #最高工资
    conn = pymysql.connect(
        host='127.0.0.1',
        user='root',
        password='root',
        port=3306,
        charset='utf8',
        db='boss'
    )  # 链接数据库
    cur = conn.cursor()
    sql = "SELECT AVG(money1) FROM (SELECT SUBSTRING_INDEX(money,'-',-1) as money1 FROM `%s`) as t1" % (kw)
    cur.execute(sql)
    highs = cur.fetchall()
    high = []
    for datas in highs:
        high.append(datas[0])
        high = list(map(int, high))
    cur.close()
    conn.close()
    avg = (low[0]+high[0])/2

    #学历需求
    #高中
    conn = pymysql.connect(
        host='127.0.0.1',
        user='root',
        password='root',
        port=3306,
        charset='utf8',
        db='boss'
    )  # 链接数据库
    cur = conn.cursor()
    sql = "SELECT COUNT(*) from `%s` WHERE exp LIKE '%%高中%%';" % (kw)
    cur.execute(sql)
    edu = cur.fetchall()
    gz = []
    for datas in edu:
        gz.append(datas[0])
    cur.close()
    conn.close()
    #大专
    conn = pymysql.connect(
        host='127.0.0.1',
        user='root',
        password='root',
        port=3306,
        charset='utf8',
        db='boss'
    )  # 链接数据库
    cur = conn.cursor()
    sql = "SELECT COUNT(*) from `%s` WHERE exp LIKE '%%大专%%';" % (kw)
    cur.execute(sql)
    edu = cur.fetchall()
    dz = []
    for datas in edu:
        dz.append(datas[0])
    cur.close()
    conn.close()
    #本科
    conn = pymysql.connect(
        host='127.0.0.1',
        user='root',
        password='root',
        port=3306,
        charset='utf8',
        db='boss'
    )  # 链接数据库
    cur = conn.cursor()
    sql = "SELECT COUNT(*) from `%s` WHERE exp LIKE '%%本科%%';"%(kw)
    cur.execute(sql)
    edu = cur.fetchall()
    bk = []
    for datas in edu:
        bk.append(datas[0])
    cur.close()
    conn.close()
    #研究生
    conn = pymysql.connect(
        host='127.0.0.1',
        user='root',
        password='root',
        port=3306,
        charset='utf8',
        db='boss'
    )  # 链接数据库
    cur = conn.cursor()
    sql = "SELECT COUNT(*) from `%s` WHERE exp LIKE '%%研究生%%';" % (kw)
    cur.execute(sql)
    edu = cur.fetchall()
    yjs = []
    for datas in edu:
        yjs.append(datas[0])
    cur.close()
    conn.close()
    #硕士
    conn = pymysql.connect(
        host='127.0.0.1',
        user='root',
        password='root',
        port=3306,
        charset='utf8',
        db='boss'
    )  # 链接数据库
    cur = conn.cursor()
    sql = "SELECT COUNT(*) from `%s` WHERE exp LIKE '%%硕士%%';" % (kw)
    cur.execute(sql)
    edu = cur.fetchall()
    ss = []
    for datas in edu:
        ss.append(datas[0])
    cur.close()
    conn.close()
    #博士
    conn = pymysql.connect(
        host='127.0.0.1',
        user='root',
        password='root',
        port=3306,
        charset='utf8',
        db='boss'
    )  # 链接数据库
    cur = conn.cursor()
    sql = "SELECT COUNT(*) from `%s` WHERE exp LIKE '%%博士%%';" % (kw)
    cur.execute(sql)
    edu = cur.fetchall()
    bs = []
    for datas in edu:
        bs.append(datas[0])
    cur.close()
    conn.close()
    #学历不限
    conn = pymysql.connect(
        host='127.0.0.1',
        user='root',
        password='root',
        port=3306,
        charset='utf8',
        db='boss'
    )  # 链接数据库
    cur = conn.cursor()
    sql = "SELECT COUNT(*) from `%s` WHERE exp LIKE '%%学历不限%%';" % (kw)
    cur.execute(sql)
    edu = cur.fetchall()
    bx = []
    for datas in edu:
        bx.append(datas[0])
    cur.close()
    conn.close()



    #标签关键词词云
    conn = pymysql.connect(
        host='127.0.0.1',
        user='root',
        password='root',
        port=3306,
        charset='utf8',
        db='boss'
    )  # 链接数据库
    cur = conn.cursor()
    sql = 'select tags from `%s`' % (kw)
    cur.execute(sql)
    data = cur.fetchall()
    text = []
    for cd in data:
        text.append(cd[0])
        # print(item[0])
        datas = ' '.join(text)
    print(len(text))
    cur.close()
    conn.close()
    wc = WordCloud(
        background_color='white',
        # mask=img_array,
        font_path="msyh.ttc",
        # stopwords=exclide
        width=600, height=600,
        min_font_size=10,
        max_words=500,
        max_font_size=400
    )
    wc.generate_from_text(datas)
    # 绘图
    fig = plt.figure(1)
    plt.imshow(wc)
    plt.axis('off')  # 是否显示坐标轴
    # plt.show()  # 显示生成的词云图片
    plt.savefig(f'./static/assets/img/{kw}.jpg', dpi=100)  # 输出词云图片

    #公司排名
    conn = pymysql.connect(
        host='127.0.0.1',
        user='root',
        password='root',
        port=3306,
        charset='utf8',
        db='boss',
    )  # 链接数据库
    cur = conn.cursor()
    sql = 'select (@i :=@i + 1) AS No,a,b from (select company_name as a,count(*) as b FROM `%s` group by company_name order by count(*) DESC) as c,(SELECT @i := 0) AS it LIMIT 12 '%(kw)
    cur.execute(sql)
    company_name = cur.fetchall()
    cur.close()
    conn.close()


    # 福利关键词词云
    conn = pymysql.connect(
        host='127.0.0.1',
        user='root',
        password='root',
        port=3306,
        charset='utf8',
        db='boss'
    )  # 链接数据库
    cur = conn.cursor()
    sql = 'select boon from `%s`' % (kw)
    cur.execute(sql)
    data = cur.fetchall()
    text = []
    for cd in data:
        text.append(cd[0])
        # print(item[0])
        datas = ' '.join(text)
    print(len(text))
    cur.close()
    conn.close()
    wc = WordCloud(
        background_color='white',
        # mask=img_array,
        font_path="msyh.ttc",
        # stopwords=exclide
        width=600, height=600,
        min_font_size=10,
        max_words=500,
        max_font_size=400
    )
    wc.generate_from_text(datas)
    # 绘图
    fig = plt.figure(1)
    plt.imshow(wc)
    plt.axis('off')  # 是否显示坐标轴
    # plt.show()  # 显示生成的词云图片

    # 查询所有岗位
    conn = pymysql.connect(
        host='127.0.0.1',
        user='root',
        password='root',
        port=3306,
        charset='utf8',
        db='boss',
    )  # 链接数据库
    cur = conn.cursor()
    sql = 'SHOW TABLES FROM boss'
    cur.execute(sql)
    data = cur.fetchall()
    name = []
    for datas in data:
        name.append(datas[0])
    name = '  '.join(name)
    cur.close()
    conn.close()

    plt.savefig(f'./static/assets/img/{kw}福利.jpg', dpi=100)  # 输出词云图片

    return render_template('table1.html', items=item,kw = kw,low = low,high = high,avg=avg,bk=bk,gz=gz,dz=dz,bs=bs,ss=ss,yjs=yjs,bx=bx,company_names=company_name,name = name)

@app.route('/table',methods={'POST'})
def search():
    if request.form.get('question')==None:
        kw = 'python'
    else:
        kw = request.form.get('question')
    # if len(kw)==0:
    # kw = "python"
    conn = pymysql.connect(
        host='127.0.0.1',
        user='root',
        password='root',
        port=3306,
        charset='utf8',
        db='boss'
    )  # 链接数据库
    cur = conn.cursor()
    S = request.values.get('question')
    sql = 'select * from `%s`'%(kw)
    cur.execute(sql)
    item = cur.fetchall()
    cur.close()
    conn.close()
    # 最低工资
    conn = pymysql.connect(
        host='127.0.0.1',
        user='root',
        password='root',
        port=3306,
        charset='utf8',
        db='boss'
    )  # 链接数据库
    cur = conn.cursor()
    sql = "SELECT AVG(money1) FROM (SELECT SUBSTRING_INDEX(money,'-',1) as money1 FROM `%s`) as t1" % (kw)
    cur.execute(sql)
    lows = cur.fetchall()
    low = []
    for datas in lows:
        low.append(datas[0])
        low = list(map(int, low))
    cur.close()
    conn.close()
    # 最高工资
    conn = pymysql.connect(
        host='127.0.0.1',
        user='root',
        password='root',
        port=3306,
        charset='utf8',
        db='boss'
    )  # 链接数据库
    cur = conn.cursor()
    sql = "SELECT AVG(money1) FROM (SELECT SUBSTRING_INDEX(money,'-',-1) as money1 FROM `%s`) as t1" % (kw)
    cur.execute(sql)
    highs = cur.fetchall()
    high = []
    for datas in highs:
        high.append(datas[0])
        high = list(map(int, high))
    cur.close()
    conn.close()
    avg = (low[0] + high[0]) / 2
    # 学历需求
    # 高中
    conn = pymysql.connect(
        host='127.0.0.1',
        user='root',
        password='root',
        port=3306,
        charset='utf8',
        db='boss'
    )  # 链接数据库
    cur = conn.cursor()
    sql = "SELECT COUNT(*) from `%s` WHERE exp LIKE '%%高中%%';" % (kw)
    cur.execute(sql)
    edu = cur.fetchall()
    gz = []
    for datas in edu:
        gz.append(datas[0])
    cur.close()
    conn.close()
    # 大专
    conn = pymysql.connect(
        host='127.0.0.1',
        user='root',
        password='root',
        port=3306,
        charset='utf8',
        db='boss'
    )  # 链接数据库
    cur = conn.cursor()
    sql = "SELECT COUNT(*) from `%s` WHERE exp LIKE '%%大专%%';" % (kw)
    cur.execute(sql)
    edu = cur.fetchall()
    dz = []
    for datas in edu:
        dz.append(datas[0])
    cur.close()
    conn.close()
    # 本科
    conn = pymysql.connect(
        host='127.0.0.1',
        user='root',
        password='root',
        port=3306,
        charset='utf8',
        db='boss'
    )  # 链接数据库
    cur = conn.cursor()
    sql = "SELECT COUNT(*) from `%s` WHERE exp LIKE '%%本科%%';" % (kw)
    cur.execute(sql)
    edu = cur.fetchall()
    bk = []
    for datas in edu:
        bk.append(datas[0])
    cur.close()
    conn.close()
    # 研究生
    conn = pymysql.connect(
        host='127.0.0.1',
        user='root',
        password='root',
        port=3306,
        charset='utf8',
        db='boss'
    )  # 链接数据库
    cur = conn.cursor()
    sql = "SELECT COUNT(*) from `%s` WHERE exp LIKE '%%研究生%%';" % (kw)
    cur.execute(sql)
    edu = cur.fetchall()
    yjs = []
    for datas in edu:
        yjs.append(datas[0])
    cur.close()
    conn.close()
    # 硕士
    conn = pymysql.connect(
        host='127.0.0.1',
        user='root',
        password='root',
        port=3306,
        charset='utf8',
        db='boss'
    )  # 链接数据库
    cur = conn.cursor()
    sql = "SELECT COUNT(*) from `%s` WHERE exp LIKE '%%硕士%%';" % (kw)
    cur.execute(sql)
    edu = cur.fetchall()
    ss = []
    for datas in edu:
        ss.append(datas[0])
    cur.close()
    conn.close()
    # 博士
    conn = pymysql.connect(
        host='127.0.0.1',
        user='root',
        password='root',
        port=3306,
        charset='utf8',
        db='boss'
    )  # 链接数据库
    cur = conn.cursor()
    sql = "SELECT COUNT(*) from `%s` WHERE exp LIKE '%%博士%%';" % (kw)
    cur.execute(sql)
    edu = cur.fetchall()
    bs = []
    for datas in edu:
        bs.append(datas[0])
    cur.close()
    conn.close()
    # 学历不限
    conn = pymysql.connect(
        host='127.0.0.1',
        user='root',
        password='root',
        port=3306,
        charset='utf8',
        db='boss'
    )  # 链接数据库
    cur = conn.cursor()
    sql = "SELECT COUNT(*) from `%s` WHERE exp LIKE '%%学历不限%%';" % (kw)
    cur.execute(sql)
    edu = cur.fetchall()
    bx = []
    for datas in edu:
        bx.append(datas[0])
    cur.close()
    conn.close()
    # 词云

    #岗位关键词
    conn = pymysql.connect(
        host='127.0.0.1',
        user='root',
        password='root',
        port=3306,
        charset='utf8',
        db='boss'
    )  # 链接数据库
    cur = conn.cursor()
    sql = 'select tags from `%s`' % (kw)
    cur.execute(sql)
    data = cur.fetchall()
    text = []
    for cd in data:
        text.append(cd[0])
        # print(item[0])
        datas = ' '.join(text)
    print(len(text))
    cur.close()
    conn.close()
    wc = WordCloud(
        background_color='white',
        # mask=img_array,
        font_path="msyh.ttc",
        # stopwords=exclide
        width=600, height=600,
        min_font_size=10,
        max_words=500,
        max_font_size=400
    )
    wc.generate_from_text(datas)
    # 绘图
    fig = plt.figure(1)
    plt.imshow(wc)
    plt.axis('off')  # 是否显示坐标轴
    # plt.show()  # 显示生成的词云图片
    plt.savefig(f'./static/assets/img/{kw}.jpg', dpi=100)  # 输出词云图片



    #公司排名
    conn = pymysql.connect(
        host='127.0.0.1',
        user='root',
        password='root',
        port=3306,
        charset='utf8',
        db='boss',
    )  # 链接数据库
    cur = conn.cursor()
    sql = 'select (@i :=@i + 1) AS No,a,b from (select company_name as a,count(*) as b FROM `%s` group by company_name order by count(*) DESC) as c,(SELECT @i := 0) AS it LIMIT 12 '%(kw)
    cur.execute(sql)
    company_name = cur.fetchall()
    cur.close()
    conn.close()

    # 福利关键词
    conn = pymysql.connect(
        host='127.0.0.1',
        user='root',
        password='root',
        port=3306,
        charset='utf8',
        db='boss'
    )  # 链接数据库
    cur = conn.cursor()
    sql = 'select boon from `%s`' % (kw)
    cur.execute(sql)
    data = cur.fetchall()
    text = []
    for cd in data:
        text.append(cd[0])
        # print(item[0])
        datas = ' '.join(text)
    print(len(text))
    cur.close()
    conn.close()
    wc = WordCloud(
        background_color='white',
        # mask=img_array,
        font_path="msyh.ttc",
        # stopwords=exclide
        width=600, height=600,
        min_font_size=10,
        max_words=500,
        max_font_size=400
    )
    wc.generate_from_text(datas)
    # 绘图
    fig = plt.figure(1)
    plt.imshow(wc)
    plt.axis('off')  # 是否显示坐标轴
    # plt.show()  # 显示生成的词云图片
    plt.savefig(f'./static/assets/img/{kw}福利.jpg', dpi=100)  # 输出词云图片

    # 查询所有岗位
    conn = pymysql.connect(
        host='127.0.0.1',
        user='root',
        password='root',
        port=3306,
        charset='utf8',
        db='boss',
    )  # 链接数据库
    cur = conn.cursor()
    sql = 'SHOW TABLES FROM boss'
    cur.execute(sql)
    data = cur.fetchall()
    name = []
    for datas in data:
        name.append(datas[0])
    name = '  '.join(name)
    cur.close()
    conn.close()
    return render_template('table.html', items=item,kw = kw,low = low,high = high,avg=avg,bk=bk,gz=gz,dz=dz,bs=bs,ss=ss,yjs=yjs,bx=bx,company_names=company_name,name=name)

if __name__ == '__main__':
    app.run(debug=True)

