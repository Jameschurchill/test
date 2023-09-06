import time
a=time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
#localtime = time.localtime(time.time())
print (repr(a))
sql="delete from test where date='{}'".format(a)
sql1="delete from test where date={}".format(a)
sql2="delete from test where date='{abc}'".format(abc=a)
sql3="delete from test where date='%s'"%(a)
print("sql:"+sql)
print("sql1:"+sql1)
print("sql2:"+sql2)
print("sql3:"+sql3)



D:\pycharm_project_64\venv\Scripts\python.exe D:/pycharm_project_64/time.py
'2019-03-05 15:34:04'
sql:delete from test where date='2019-03-05 15:34:04'
sql1:delete from test where date=2019-03-05 15:34:04
sql2:delete from test where date='2019-03-05 15:34:04'
sql3:delete from test where date='2019-03-05 15:34:04'

Process finished with exit code 0
