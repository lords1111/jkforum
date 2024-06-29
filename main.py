import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
import re
import pymysql
import time
#一级网站
first_url="https://www.jkforum.net/p/forum-51-1.html"
proxies={
    'http':"http://127.0.0.1:2080",
    'https':"http://127.0.0.1:2080"
}
headers={
        'User-Agent': f'{UserAgent().Chrome}'
    }


#获取子版块
def two():
    res=requests.get(url=first_url,proxies=proxies,headers=headers)
    soup=BeautifulSoup(res.text,'html.parser')
    second_element=soup.find_all(id="subforum_51")
    pattern=re.compile(r'.*?<a href="forum-(.*?)-1.html"><img align="left" alt="" src=".*?" style="">(.*?)</a>',re.S)
    second_urls=pattern.findall(str(second_element[0]))
    second_urls_dictionary={n:"https://www.jkforum.net/p/forum-"+u+"-" for u,n in second_urls}
    #print(second_urls_dictionary)
    return second_urls_dictionary

#获取合集
def three(second_url):
    res=requests.get(url=second_url,proxies=proxies,headers=headers)
    soup=BeautifulSoup(res.text,'html.parser')
    third_element=soup.find_all(id='waterfall')
    #print(third_element)
    pattern=re.compile(r'.*?<a href="(thread-.*?.html)" onclick="atarget\(this\)".*?title="(.*?)">',re.S)
    try:
        third_urls=pattern.findall(str(third_element[0]))
    except:
        print("未找到")
    third_urls_dictionary={n:"https://www.jkforum.net/p/"+u for u,n in third_urls}
    #print(third_urls_dictionary)
    return third_urls_dictionary

#获取合集图片链接
def four(third_url):
    res=requests.get(url=third_url,proxies=proxies,headers=headers)
    soup=BeautifulSoup(res.text,'html.parser')
    forth_element=soup.find_all('ignore_js_op')
    pattern=re.compile(r'.*?<a href="(forum.php\?mod=attachment&amp;aid=.*?&amp;nothumb=yes)".*?',re.S)
    forth_urls=pattern.findall(str(forth_element))
    forth_urls=["https://www.jkforum.net/"+f.replace("&amp;","&") for f in forth_urls]
    #print(forth_urls)
    return forth_urls




def mysql(sub,second_url,page):
    conn = pymysql.connect(
        host='localhost',		# 主机名（或IP地址）
        port=3306,				# 端口号，默认为3306
        user='root',			# 用户名
        password='xxxxx',	# 密码
        charset='utf8mb4'  		# 设置字符编码
    )
    cursor = conn.cursor()
    cursor.execute("CREATE DATABASE IF NOT EXISTS forum")
    conn.select_db("forum")
    init=f'''
        CREATE TABLE IF NOT EXISTS {sub.replace(" - ","_")} (              
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    title VARCHAR(255) NOT NULL UNIQUE,
                    url VARCHAR(255) NOT NULL 
                )'''
    cursor.execute(init)
    conn.commit()
    second_url=second_url+f'{page}.html'
    print(second_url)
    third_urls_dictionary=three(second_url)
    
    for title in third_urls_dictionary:
        third_url=third_urls_dictionary[title]
        forth_urls=four(third_url)
        for url,i in zip(forth_urls,range(1,len(forth_urls)+1)):
            query=f"insert into {sub.replace(' - ','_')} (title,url) values ('{title}-{i}','{url}')"
            print(sub+"~~~"+title+"~~~"+url)
            try:
                cursor.execute(query)
                conn.commit()
            except:
                print("插入失败")

import threading
class MyThread(threading.Thread):
    def __init__(self,sub,second_url,page):
        super().__init__()
        self.sub=sub
        self.url=second_url
        self.page=page

    def run(self):
        mysql(self.sub,self.url,self.page)

def main():
    second_urls_dictionary=two()
    sublist=[sub for sub in second_urls_dictionary]
    print(sublist)
    xs=input("选择版块,以‘,’分隔开：").split(",")
    page=int(input("选择第几页："))
    xi=[int(x) for x in xs]
    t_list=[]
    for x in xi:
        sub=sublist[x-1]
        thread=MyThread(sub,second_urls_dictionary[sub],page)
        thread.start()
        t_list.append(thread)
    for i in t_list:
        i.join()   

if __name__=='__main__':
    main()
    #print(three('https://www.jkforum.net/p/forum-1411-2.html'))
    