# -*- coding = utf-8 -*-
# @Time : 2021/11/28 19:12
# @Author : wjj
# @File : test3.py
# @Software : PyCharm
from selenium import webdriver
import pymysql
from urllib import parse



#创建数据库表
def init_db():
    conn = pymysql.connect(
        host='127.0.0.1',
        user='root',
        password='root',
        port=3306,
        charset='utf8',
        db='boss'
    ) #链接数据库
    sql = 'CREATE TABLE `%s`(`id` int(11) NOT NULL AUTO_INCREMENT,`name` VARCHAR(255) DEFAULT NULL,`area` VARCHAR(255) DEFAULT NULL,`company_name` VARCHAR(255) DEFAULT NULL,`company_type` VARCHAR(255) DEFAULT NULL,`money` VARCHAR(255) DEFAULT NULL,`exp` VARCHAR(255) DEFAULT NULL,`tags` VARCHAR(255) DEFAULT NULL,`boon` VARCHAR(255) DEFAULT NULL,PRIMARY KEY (`id`)) ENGINE=InnoDB DEFAULT CHARSET=utf8;'%(KeyWord) #创建数据库表
    cursor = conn.cursor()
    cursor.execute(sql)
    # print(sql)
    conn.close()



#插入数据
def saveDB(datalist):
    init_db() #创建表
    conn = pymysql.connect(
        host='127.0.0.1',
        user='root',
        password='root',
        port=3306,
        charset='utf8',
        db='boss'
    )
    #创建游标
    cursor = conn.cursor()
    i = 0
    for ex in datalist:
        i = i+1
        #工作名称
        name = ex[0]
        #工作地点
        area = ex[1]
        #公司名称
        company_name = ex[2]
        #公司类型
        company_type = ex[3]
        #薪资待遇
        money = ex[4]
        #经验学历
        exp = ex[5]
        #标签
        tags = ex[6]
        #福利待遇
        boon = ex[7]
        try:
            sql = 'insert into `%s`(name,area,company_name,company_type,money,exp,tags,boon)values("{}","{}","{}","{}","{}","{}","{}","{}")'.format(
                name,area,company_name,company_type,money,exp,tags,boon)%(KeyWord)
            cursor.execute(sql)
            conn.commit()
            print(f"正在保存第{i}条数据")
            # print(sql)
        except:
            print("数据有问题"+name)
    cursor.close()
    conn.close()





path='chromedriver.exe'
drive = webdriver.Chrome(path)
KeyWord = input("请输入你要搜索的岗位关键字")
KeyWords = parse.quote(parse.quote(KeyWord))
# print(KeyWords)
drive.get("https://www.zhipin.com/c101280600/?query="+KeyWords+"&page=1&ka=page-")
drive.implicitly_wait(10)
datalist = []
def get_job_info():
    lis = drive.find_elements_by_css_selector('.job-list li')
    for li in lis:
        data = []
        # 工作名称
        name = li.find_element_by_css_selector('.job-name a').text
        data.append(name)
        # 工作地点
        area = li.find_element_by_css_selector('.job-area').text
        data.append(area)
        # 公司名称
        company_name = li.find_element_by_css_selector('.company-text .name a').text
        data.append(company_name)
        # 公司类型
        company_type = li.find_element_by_css_selector('.company-text p a').text
        data.append(company_type)
        # 薪资待遇
        money = li.find_element_by_css_selector('.red').text
        money = ''.join(money).replace("13薪", '').replace('14薪', '').replace('16薪', '').replace('·', '')
        if (len(money) > 6): #个别薪资格式不统一，强行用下面代替
            money = "6-8K"
        money = ''.join(money).replace('-','000-').replace('K','000')
        data.append(money)
        # 经验学历
        exp = li.find_element_by_css_selector('.job-limit p').text
        data.append(exp)
        # 标签
        tags = li.find_element_by_css_selector('.tags span').text
        data.append(tags)
        # 福利待遇
        boon = li.find_element_by_css_selector('.info-desc').text
        data.append(boon)
        #tags = [tag.find_element_by_css_selector('.tag-item') for tag in tags]
        # print(name,area,company_name,company_type,money,exp,tags,boon)
        datalist.append(data)
        # nonextpage = drive.find_element_by_css_selector(".page .disabled")
        print(data)
    return datalist



if __name__ == '__main__':
    # main()
    # datalist = get_job_info()
    # dbpath = f"{KeyWord}成都招聘数据.db"
    #init_db("test.db")
    for page in range(1,11):
        print(f'正在爬取第{page}页的数据内容')
        get_job_info()
        try:
            drive.find_element_by_css_selector(".page .disabled")
            saveDB(datalist)
            break
        except:
            drive.find_element_by_css_selector(".next").click()
    drive.quit()