import os
import requests
import re
from bs4 import BeautifulSoup

def check_dir(dir):
    if not os.path.isdir(dir):
        os.mkdir(dir)
        print('create folder:', dir)

#定義網址
base_url = "https://tw.news.yahoo.com"
url = "https://tw.news.yahoo.com/sports/archive/"

#向網址要回網頁原始碼，並透過 BeautifulSoup 解析
res = requests.get(url)
soup = BeautifulSoup(res.text, 'html.parser')

start = 0
pages = range(start, start+1)  

sports_all = []
for page in pages:
    print(url + str(page) + ".html")
    yahoo_r = requests.get(url + str(page) + ".html")
    yahoo_soup = BeautifulSoup(yahoo_r.text, 'html.parser')
    sports = yahoo_soup.findAll('h3')
    sports_all.append(sports)

len(sports_all)
links = []
for finance in sports_all:
    for info in finance:
        link = ""
        try:
            link = info.findAll('a', href=True)[0]
            title = link.get_text()
            print(title)
            # filter out 一覽表
            if title.find("一覽表") < 0 and link.get('href') != '#':
                full_url = base_url + link.get("href") 
                links.append( (title, full_url) )
                print(full_url)
        except:
            print("exception")
            link = None
print(len(links))

cwd = os.getcwd()
output = os.path.join(cwd, "output")
check_dir(output)

total = start + len(links)
current = start
restart = 0
index_file_path = 'index-{start}.txt'.format(start=current)
index_file_path = os.path.join(output, index_file_path)
print(index_file_path)

with open(index_file_path, 'w') as index_file:
    for (title, url) in links:
        news = requests.get(url)
        single_news = BeautifulSoup(news.text, 'html.parser')
        try:
            current += 1
            if current > restart:
                print(f"({current}/{total}) {title}")
                index_file.write(f"({current}/{total}) {title}\n")
                article = single_news.findAll('p')
                file_path = 'article-{current}-{total}.txt'.format(current=current, total=total)
                file_path = os.path.join(output, file_path)
                print(file_path)
                try:
                    index_file.write(file_path + '\n')
                except:
                    print('error!')
                with open(file_path, 'w') as textfile:
                    for paragraph in article:
                        try:
                            textfile.write(paragraph.text + '\n')
                        except:
                            print('error!')
                    textfile.close()
            else:
                print("done before") 
        except:
            print("exception")
            continue
    index_file.close()
print("download completed")