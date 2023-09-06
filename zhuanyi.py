a="abc"
b="i love {aa} china".format(aa=a)
print(b)


import time
a=time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
#localtime = time.localtime(time.time())
print (a)
sql="delete from test where date='{}'".format(a)
sql1="delete from test where date={}".format(a)
print(sql)
print(sql1)
输出结果：
2019-01-28 10:22:52
delete from test where date='2019-01-28 10:22:52'
delete from test where date=2019-01-28 10:22:52




name = 'zhangsan'
age = 25
price = 'years'
print('my name is %s'%(name))
print('i am %s years old'%(age))#如果有多个变量，引号里就用多个%，然后引号外用一个%和一个( , )代替
print('i am %s %s old'%(age,price))
print('i am {} years old'.format(age))
print('i am {c} {d} old'.format(c=age,d=price))

my name is zhangsan
i am 25 years old
i am 25 years old
i am 25 years old