import pandas as pd
import os
import glob
import pypinyin
def hp(word):
    s = ''
    for i in pypinyin.pinyin(word, style=pypinyin.NORMAL):
        s += ''.join(i)
    return s
def csv_to_xlsx_pd():
   filelist = glob.glob(r'E:\excel\*.xlsx')#获取excel列表
   for    filename in filelist:
       line=os.path.basename(filename)#获取路径的文件名
       line1=hp(line.split('.')[0])#汉字转拼音
       print(line1)
       csv = pd.pandas.read_excel(filename,sheet_name= 'Sheet1')
       csv.to_csv(r'E:\excel\%s.csv'%(line1),index=False,quotechar='"',doublequote=True,header=False,encoding='utf-8')
if __name__ == '__main__':
    csv_to_xlsx_pd()
