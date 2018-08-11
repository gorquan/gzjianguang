# author:gorquan
# date：2018-8-11
from urllib import request
from bs4 import BeautifulSoup as bs
import time
import os
import re
'''

    用来爬取网站网页
    实现功能：url深度抓取，保存每个页面的css、html、js等文件
'''


# 深度爬取当前页面子网站子网站
def get_urls(url, baseurl, urls):
    with request.urlopen(url) as f:
        data = f.read().decode('utf-8')
        link = bs(data).find_all('a')
        for i in link:
            suffix = i.get('href')
            # 设置排除写入的子连接
            if suffix == '#' or suffix == '#carousel-example-generic' or 'javascript:void(0)' in suffix:
                continue
            else:
                # 构建urls
                childurl = baseurl + suffix
                if childurl not in urls:
                    urls.append(childurl)


# 抓取全站url
def getallUrl(url, baseurl, urls):
    get_urls(url, baseurl, urls)
    end = len(urls)
    start = 0
    while(True):
        if start == end:
            break
        for i in range(start, end):
            get_urls(urls[i], baseurl, urls)
            time.sleep(1)
        start = end
        end = len(urls)

# 创建文件夹
def mkdir(title, basedir):
    path = basedir + '\\' + title
    if os.path.exists(path):
        os.rmdir(path)
    os.mkdir(path)
    print(path + " 目录创建成功")


# 获取每个页面代码以及获取页面上的css，js，img路径
def get_source(url, path):
    with request.urlopen(url) as f:
        html_source = f.read().decode()
        # 添加时间截以区分文件夹名字
        timeStr = str(int(time.time()))
        pattertitile = '<title>(.*?)</title>'
        patterncss = '<link rel="stylesheet" href="(.*?)"'
        patternjs = '<script src="(.*?)"'
        patternimg = '<img src="(.*?)"'
        titleStr = re.compile(pattertitile, re.S).findall(html_source)[0]
        if '|' in titleStr:
            title = (titleStr.split("|")[1]).split(' ')[1] + timeStr
        else:
            title = titleStr + timeStr
        mkdir(title, path)
        path = basedir + '\\' + title
        filename = path + '\\' + title + '.html'
        # 获取css，js，img地址
        cssHerf = re.compile(patterncss, re.S).findall(html_source)
        jsHref = re.compile(patternjs, re.S).findall(html_source)
        imgHref = re.compile(patternimg, re.S).findall(html_source)
        # 保存html
        try:
            with open(filename, 'w') as f:
                f.write(html_source)
        except:
            print("文件无法保存，请检查参数配置")
            exit(1)
        print(title + ".html文件保存成功")
        # 保存css，js，img
        save_css(cssHerf, path)
        save_js(jsHref, path)
        save_img(imgHref, path)
        print(url + "源码保存成功")
        time.sleep(1)


# 保存css文件
def save_css(href, path):
    for i in range(0, len(href)):
        url = "http://www.gzjianguang.com" + href[i]
        patternCssTitle = '(/?.*?.css?)'
        filename = path + '\\' + re.compile(patternCssTitle, re.S).findall(url)[1][1:]
        try:
            with request.urlopen(url) as w:
                css_source = w.read().decode()
                with open(filename, 'w') as f:
                    f.write(css_source)
                print(re.compile(patternCssTitle, re.S).findall(url)[1][1:] + " css文件保存成功！")
                time.sleep(1)
        except:
            print("该" + re.compile(patternCssTitle, re.S).findall(url)[1][1:] + " css文件无法下载")


# 保存js文件
def save_js(href, path):
    for i in range(0, len(href)):
        url = "http://www.gzjianguang.com" + href[i]
        filename = path + '\\' + href[i].split('/')[-1]
        try:
            with request.urlopen(url) as w:
                js_source = w.read().decode()
                with open(filename, 'w') as f:
                    f.write(js_source)
                print(href[i].split('/')[-1] + " js文件保存成功")
                time.sleep(1)
        except:
            print("该" + href[i].split('/')[-1] + " js文件无法下载")
            continue


# 保存img文件
def save_img(href, path):
    for i in range(0, len(href)):
        url = "http://www.gzjianguang.com" + href[i]
        filename = path + '\\' + href[i].split('/')[-1]
        try:
            with request.urlopen(url) as w:
                img_source = w.read()
                with open(filename, 'wb') as f:
                    f.write(img_source)
                print(href[i].split('/')[-1] + " 图像文件保存成功")
                time.sleep(1)
        except:
            print("该" + href[i].split('/')[-1] + " 图像无法下载")
            continue


if __name__ == '__main__':
    # 抓取网址
    url = 'http://www.gzjianguang.com'
    # 相对路径地址
    baseurl = 'http://www.gzjianguang.com'
    # 文件保存位置
    basedir = r'E:\pythonCode\gzjianguang'
    urls = []
    # 获取所有地址
    getallUrl(url, baseurl, urls)
    # 获取代码
    for u in urls:
        get_source(u,basedir)

