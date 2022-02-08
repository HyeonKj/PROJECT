# -*- coding: utf-8 -*-
"""
Created on Mon Feb  7 15:18:51 2022

@author: user
"""
import pymysql
import requests
import bs4


class craw:
    def __init__(self,target_url):
        self.url = target_url

    def get_bs4(self):
        res = requests.get(self.url)
        html_str = res.text
        return bs4.BeautifulSoup(html_str, features='lxml')

    def get_bs4_headers(self,engine):
        headers = {'User-Agent': engine}
        res = requests.get(self.url, headers=headers)
        html_str = res.text
        return bs4.BeautifulSoup(html_str)

    def get_primary_key_data(self,pg_data,col_idx):
        primary_key = []
        for i in pg_data:
            primary_key.append(i[col_idx])
        return primary_key

class enter_sql:
    def __init__(self,host,user,password,db,charset): # class 인풋 변수
        self.conn = pymysql.connect(host=host,user=user,password=password,
                       db=db,charset=charset)
        self.cur = self.conn.cursor()

    def query_execute(self,query):
        self.cur.execute(query)

    def insert_execute(self,sql,parms):
        self.cur.execute(sql,parms)

    def exit_sql(self):
        self.conn.commit()
        self.conn.close()

    def data_call(self,columns,table):
        column = ''
        for i in columns:
            column += i + ','
        column = column.strip(',')
        data = []
        self.cur.execute(f'select {column} from {table}')
        while 1:
            row = self.cur.fetchone()
            if row == None:
                break
            temp = []
            for i in range(len(columns)):
                temp.append(row[i])
            data.append(temp)
        for i in data:
            print(i)


# craw company info
myCraw = craw(f'http://kind.krx.co.kr/corpgeneral/corpList.do?method=download&searchType=13')
bs_obj = myCraw.get_bs4()
data_head = bs_obj.find_all('th')
data = bs_obj.find_all('td')

columns = [i.text for i in data_head]
columns
# caution
temp = []
for i in data:
    temp.append(i.text)

page_data = []
temp = []
target = ['\r','\n','\t']
for i in data:
    if len(temp) == len(columns):
        page_data.append(temp)
        temp = []
    if len(temp) == 7:
        x = i.text
        for j in target:
            x = x.replace(j,'')
        temp.append(x)
    else:
        temp.append(i.text)
page_data[0]


# company code
primary_key = myCraw.get_primary_key_data(page_data,1)
primary_key

# craw price info
price_info = []
i = 1
engine = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.99 Safari/537.36'
for company_code in primary_key:
    url = 'http://finance.naver.com/item/sise_day.nhn?code='+company_code
    myCraw = craw(url)
    bs_obj = myCraw.get_bs4_headers(engine)
    data = bs_obj.find_all('span',{'class':'tah p11'})
    price_info.append(data[0].text)
    print(f'success load {i}/{len(primary_key)}')
    i += 1
print(price_info)


# sql

mysql_mine = enter_sql('localhost','root','1111','INVESTAR','utf8')
mysql_mine.query_execute(f'create table if not exists company'
            f'({columns[0]} char(25),'
            f'{columns[1]} char(6) primary key,'
            f'{columns[2]} char(50),'
            f'{columns[3]} LONGTEXT,'
            f'{columns[4]} char(10),'
            f'{columns[5]} char(3),'
            f'{columns[6]} LONGTEXT,'
            f'{columns[7]} char(50),'
            f'{columns[8]} char(10))')
mysql_mine.query_execute('ALTER DATABASE investar CHARACTER SET = utf8mb4 COLLATE = utf8mb4_unicode_ci;')
mysql_mine.query_execute('ALTER TABLE company CONVERT TO CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;')
sql = """insert into company values (%s, %s, %s, %s, %s, %s, %s, %s, %s);"""
for i in page_data:
    mysql_mine.insert_execute(sql,(i[0],i[1],i[2],i[3],i[4],i[5],i[6],i[7],i[8]))
mysql_mine.exit_sql()

#
mysql_mine = enter_sql('localhost','root','1111','INVESTAR','utf8')

mysql_mine.query_execute(f'create table if not exists price_info('
            f'{columns[1]} char(6),'
            f'today_price char(20))')
mysql_mine.query_execute('alter table price_info add constraint foreign key(종목코드) references company(종목코드);')
mysql_mine.query_execute('ALTER DATABASE investar CHARACTER SET = utf8mb4 COLLATE = utf8mb4_unicode_ci;')
mysql_mine.query_execute('ALTER TABLE company CONVERT TO CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;')
sql = """insert into price_info values (%s, %s);"""
for i in range(len(primary_key)):
    mysql_mine.insert_execute(sql,(primary_key[i],price_info[i]))

mysql_mine.exit_sql()

#
mysql_mine = enter_sql('localhost','root','1111','INVESTAR','utf8')
mysql_mine.data_call(['회사명','대표자명'],'company')
mysql_mine.exit_sql()
	