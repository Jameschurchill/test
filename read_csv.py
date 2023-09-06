#encoding=utf-8
import xlrd
import pandas
import datetime
from xlwt import *
#------------------读数据---------------------------------
fileName="abc.xlsx"
bk=xlrd.open_workbook(fileName)
#shxrange=range(bk.nsheets)
shxrange=bk.nsheets
print(shxrange)
try:
  sh=bk.sheet_by_name("Sheet1")
except:
  print("sheet名称错误")
  exit()
nrows=sh.nrows #获取行数
#print(nrows)
book = Workbook(encoding='utf-8')
sheet = book.add_sheet('Sheet1') #创建一个sheet
for i in range(0,nrows):
  row_data=sh.row_values(i)
  #获取第i行第3列数据
  #sh.cell_value(i,3)
  #---------写出文件到excel--------
  print("-----正在写入 "+str(i)+" 行")
  sheet.write(i,0, label = sh.cell_value(i,1)) #向第1行第1列写入获取到的值
  sheet.write(i,1, label = sh.cell_value(i,2)) #向第1行第2列写入获取到的值
book.save(r'E:\test1.xls')
df = pandas.read_excel(r'E:\test1.xls',sheet_name= 'Sheet1')
#df.dropna(axis=0, how='all', inplace=True)
#df.drop_duplicates().fillna("").to_csv(r'E:\test2.csv', index=False, encoding="utf-8", sep=",")
#df.to_csv(r'E:\test2_'+datetime.datetime.now().strftime('%Y%m%d')+'.txt',index=False,sep='',header=False,encoding='utf-8')
df.to_csv(r'E:\test2_'+datetime.datetime.now().strftime('%Y%m%d')+'.txt',index=False,quotechar='"',doublequote=True,header=False,encoding='utf-8')