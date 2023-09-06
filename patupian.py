#coding=utf-8
import random
#urllib模块提供了读取Web页面数据的接口
import urllib.request
#re模块主要包含了正则表达式
import re
#定义一个getHtml()函数
# def __init__(self):
#     self.x = 0
def mkdir(path):
 # 引入模块
 import os

 # 去除首位空格
 path = path.strip()
 # 去除尾部 \ 符号
 path = path.rstrip("\\")

 # 判断路径是否存在
 # 存在     True
 # 不存在   False
 isExists = os.path.exists(path)

 # 判断结果
 if not isExists:
  # 如果不存在则创建目录
  # 创建目录操作函数
  os.makedirs(path)

  print(path + ' 创建成功')
  return True
 else:
  # 如果目录存在则不创建，并提示目录已存在
  print(path + ' 目录已存在')
  return False
def getHtml(url):
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.103 Safari/537.36'}
    req = urllib.request.Request(url=url, headers=headers)
    page=urllib.request.urlopen(req)
    #page = urllib.request.urlopen(url)  #urllib.request.urlopen()方法用于打开一个URL地址
    html = page.read() #read()方法用于读取URL上的数据
    return html

def getImg(ddir):
    x = 0
    page=1
    for i in range(1, page+1):
          #html = getHtml("http://tieba.baidu.com/p/3412178597?pn=%s" % (i))
          html = getHtml("https://www.duotu555.com/")
          for j in ('jpg','png','gif'):
             #reg = r'src="(.+?\.%s)"'%j
             #纯粹的http链接
             reg = r'src="(http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+)"'
             imgre = re.compile(reg)     #re.compile() 可以把正则表达式编译成一个正则表达式对象.
             try:
               html = html.decode('utf-8','ignore') #python3 可以忽略utf-8编码gbk也支持
             except:
               print("can not get decode")
             imglist = re.findall(imgre,html)      #re.findall() 方法读取html 中包含 imgre（正则表达式）的数据
             #把筛选的图片地址通过for循环遍历并保存到本地
             #核心是urllib.request.urlretrieve()方法,直接将远程数据下载到本地，图片通过x依次递增命名


             for imgurl in imglist:
                 try:
                   urllib.request.urlretrieve(imgurl,ddir+'\%s.gif'% x)
                 except:
                     print("can not get picture")
                     #continue
                 else:
                     print("获得图片序号为",x)
                     x += 1
    print("总共获取图片数为:",x)

if __name__ == '__main__':
    ddir = r'D:\tupian5'
    mkdir(ddir)
    getImg(ddir)