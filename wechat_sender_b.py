#coding=utf-8
from wechat_sender import Sender
from wxpy import *
import time
#初始化机器人，选择缓存模式（扫码）
robot = Bot(cache_path=True)
#listen(robot)
#获取好友、群、公众号信息
robot.chats()
my=robot.friends().search('子非鱼')[0]
group=robot.groups().search('还扯不扯淡')[0]#发给群 group=ensure_one(robot.groups().search(u'还扯不扯淡')[0])
#group.send('Hello From Wechat Sender')
count = 0
while count < 10:
   time.sleep(10)
   my.send("hello world from Wechat ")#发给自己
   count = count + 1
   #robot.file_helper.send('Hello world!')#文件助手发送

