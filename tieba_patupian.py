#coding=utf-8
import random
#urllib模块提供了读取Web页面数据的接口
import urllib.request
#re模块主要包含了正则表达式
import re
#定义一个getHtml()函数
# def __init__(self):
#     self.x = 0
def getHtml(url):
    page = urllib.request.urlopen(url)  #urllib.request.urlopen()方法用于打开一个URL地址
    html = page.read() #read()方法用于读取URL上的数据
    return html

def getImg(ddir):
    x = 0
    page=6
    for i in range(1, page+1):
          html = getHtml("https://tieba.baidu.com/p/3406333395?see_lz=1&pn=%s" % (i))
          for j in ('jpg','png','gif'):
             reg = r'src="(.+?\.%s)"'%j
               #reg=r'src="(.+?\.jpg)"|src="(.+?\.jpg)"|src="(.+?\.gif)"'
             #reg=r'https://.[^\s]+?.jpg|https://.[^\s]+?.png|https://.[^\s]+?.gif'#正则表达式，得到图片地址
             imgre = re.compile(reg)     #re.compile() 可以把正则表达式编译成一个正则表达式对象.
             try:
               html = html.decode('utf-8') #python3
             except:
               print("can not get picture")
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
    ddir = r'D:\tupian2'
    getImg(ddir)