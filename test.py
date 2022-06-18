from urllib import parse
import requests
from lxml import etree
import pymysql
from selenium import webdriver

path = 'chromedriver.exe'
drive = webdriver.Chrome(path)

KeyWord = '爬虫'
KeyWords = parse.quote(parse.quote(KeyWord))

drive.get("https://www.zhipin.com/c101280600/?query=" + KeyWords + "&page=1&ka=page-")
drive.implicitly_wait(10)

datalist = []

def get_info():
    jobname_list = drive.find_elements_by_xpath('//div[@class="job-primary"]//span[@class="job-name"]/a')
    jobhome_list = drive.find_elements_by_xpath('//div[@class="job-primary"]//span[@class="job-area"]')
    company_list = drive.find_elements_by_xpath('//div[@class="job-primary"]//div[@class="company-text"]/h3/a')
    company_typelist = drive.find_elements_by_xpath('//div[@class="job-primary"]//div[@class="company-text"]/p/a')
    mony_list = drive.find_elements_by_xpath('//div[@class="job-primary"]//span[@class="red"]')

    limit_list=drive.find_elements_by_xpath('//div[@class="job-limit clearfix"]/p')
    tags_list=drive.find_elements_by_xpath('//div[@class="tags"]/span[1]')
    fuli_list=drive.find_elements_by_xpath('//div[@class="info-desc"]')
    for i in range(len(jobname_list)):
        data = []
        jobname = jobname_list[i].text
        jobhome = jobhome_list[i].text
        company = company_list[i].text
        company_type = company_typelist[i].text
        money = mony_list[i].text

        limit=limit_list[i].text
        tags=tags_list[i].text
        fuli=fuli_list[i].text
        if money:
            money = ''.join(money).replace("13薪", '').replace('14薪', '').replace('16薪', '').replace('·', '')
            if (len(money) > 6):  # 个别薪资格式不统一，强行用下面代替
                money = "6-8K"
            money = ''.join(money).replace('-', '000-').replace('K', '000')
        data.append(jobname)
        data.append(jobhome)
        data.append(company)
        data.append(company_type)
        data.append(money)

        data.append(limit)
        data.append(tags)
        data.append(fuli)

        datalist.append(data)
        print(data)
    return  datalist

#创建数据库表
def init_db():
    conn = pymysql.connect(
        host='127.0.0.1',
        user='root',
        password='root',
        port=3306,
        charset='utf8',
        db='bosstest'
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
        db='bosstest'
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

if __name__ == '__main__':
    for page in range(1,11):
        print(f'正在爬取第{page}页的数据内容')
        get_info()
        try:
            drive.find_element_by_xpath('//a[@class="next disabled"]')
            saveDB(datalist)
            break
        except:
            drive.find_element_by_xpath('//a[@class="next"]').click()
print(datalist)

