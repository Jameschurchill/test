# -*- coding: utf-8 -*-
"""
Created on Tue Feb 26 16:47:31 2019

@author: Administrator
"""
import os
import time
from datetime import datetime,timedelta
import pandas as pd
import xlrd
import xlsxwriter
import poplib
from wxpy import Bot
from email.parser import Parser
from email.header import decode_header
from email.utils import parseaddr
import zipfile

def read_new_data(xls):
    file = xlrd.open_workbook(xls)
    sh = file.sheet_by_name("Sheet1")
    nrows = sh.nrows 
    label = []                                             
    for i in range(nrows):
        if isinstance(sh.col_values(0)[i],str) and '统计日期' in sh.col_values(0)[i]:             
            label.append(i)
        if isinstance(sh.col_values(3)[i],str) and '合计' in sh.col_values(3)[i].replace(' ',''):
            label.append(i)
        elif isinstance(sh.col_values(0)[i],str) and '制表人' in sh.col_values(0)[i]:
            label.append(i)

    if sum(sh.col_values(12)[label[0]+3:label[1]])>2000:
        mark=1
    else:
        mark=2 
 
    df = pd.DataFrame({'company1':[86320000]+list(map(int,sh.col_values(0)[label[0]+3:label[1]])),
                       'key':[mark]*(1+len(sh.col_values(0)[label[0]+3:label[1]])),
                       'annual':[sum(sh.col_values(4)[label[0]+3:label[1]])]+sh.col_values(4)[label[0]+3:label[1]],
                       'ten':[sum(sh.col_values(8)[label[0]+3:label[1]])]+sh.col_values(8)[label[0]+3:label[1]],
                       'time':[sh.col_values(0)[label[0]][18:28]]*(label[1]-label[0]-3+1)})
    return df

def read_insu_data(xls):
    file = xlrd.open_workbook(xls)
    sh = file.sheet_by_name("Sheet1")
    nrows = sh.nrows 
    label,pay_period,single= [],[],[]                                    
    for i in range(nrows):
        if  isinstance(sh.col_values(9)[i],str) and '统计区间' in sh.col_values(9)[i]:             
            label.append(i)
              
        if  isinstance(sh.col_values(0)[i],str) and '合计' in sh.cell_value(i-1,1).replace(' ',''):
            label.append(i)
        elif isinstance(sh.col_values(0)[i],str) and '制表人' in sh.col_values(0)[i]:
            label.append(i)
    day1 = time.strptime(sh.col_values(9)[label[0]][20:30],"%Y-%m-%d")
    day2 = time.strptime('2019-01-01',"%Y-%m-%d")            
    if sum(map(int,sh.col_values(8)[label[0]+4:label[1]-1])) >240*(datetime(day1[0],day1[1],day1[2])-datetime(day1[0],day2[1],day2[2])).days:
        mark=1
    else:
        mark=2 
    for i in range(label[0]+4,label[1]-1): 
        if  isinstance(sh.cell_value(i,7),str) and sh.cell_value(i,7).replace(' ','')=='':
            pay_period.append(1)
        else:
            pay_period.append(int(sh.cell_value(i,7)))
#        print(sh.cell_value(i,0),i)
       
        single.append(sh.cell_value(i,20)+sh.cell_value(i,24))
#    print(xls,sh.col_values(0)[label[0]+4:label[1]-1])   
    df = pd.DataFrame({'company1':list(map(int,sh.col_values(0)[label[0]+4:label[1]-1])),
                       'pay_period':pay_period,
                        'single':single,
                       'key':[mark]*(label[1]-1-label[0]-4),
                       'time':[sh.cell_value(label[0],9)[20:30]]*(label[1]-1-label[0]-4)})
    
    return df
    
def compute(df0,df1,key):
    goal0=pd.DataFrame({'name':['合计','南京','无锡','徐州','常州','苏州','南通','连云港','淮安','盐城','扬州','镇江','泰州','宿迁'],
                            'annual_goal':[130000,11600,10500,9600,10400,15900,15900,6800,7500,9400,9400,7900,9300,5800],
                           'ten_goal':[26000,2320,2100,1920,2080,3180,3180,1360,1500,1880,1880,1580,1860,1160],
                           'all_annual_goal':[230000,20500,18600,17000,18400,28100,28100,12000,13300,16600,16600,14000,16500,10300],
                           'all_ten_goal':[52300,4670,4220,3860,4180,6400,6400,2740,3020,3780,3780,3180,3740,2330],
                           'all_single_goal':[134700,12000,10900,9950,10800,16500,16500,7050,7770,9740,9740,8090,9640,6020]},
                          index=[863200, 863201, 863202, 863203, 863204, 863205, 863206, 863207, 863208,863209, 863210, 863211, 863212, 863213])
    goal1=pd.DataFrame({'annual_goal':[5000,460,350,420,350,600,570,300,230,300,500,320,300,300]},
                          index=[863200, 863201, 863202, 863203, 863204, 863205, 863206, 863207, 863208,863209, 863210, 863211, 863212, 863213])
    ti = {1:sorted(list(set(df0.time)&set(df1.time))),
            2:list(set(df0.time)-set(df1.time))}
    tmp0_0 = df1[(df1['key']== key )&(df1['pay_period']==1)&(df1['time']==ti[1][0])][['company0','single']]
    tmp0_1 = df1[(df1['key']==key)&(df1['pay_period']==1)&(df1['time']==ti[1][1])][['company0','single']]
    tmp0_0 = tmp0_0.append({'company0':863200,'single':sum(tmp0_0.single)},ignore_index=True)
    tmp0_1 = tmp0_1.append({'company0':863200,'single':sum(tmp0_1.single)},ignore_index=True)
    
    
    tmp1_0 = df0[(df0['key']==key)&(df0['time']==ti[1][0])][['company0','annual','ten']]
    tmp1_1 = df0[(df0['key']==key)&(df0['time']==ti[1][1])][['company0','annual','ten']]
    
    day1 = time.strptime(ti[1][1],"%Y-%m-%d")
    day2 = time.strptime('2019-12-31',"%Y-%m-%d")
    day = (datetime(day1[0],day2[1],day2[2]) - datetime(day1[0],day1[1],day1[2])).days
    
    if key == 1:
        last = df0[(df0['key']==key)&(df0['time']==ti[2][0])][['company0','annual','ten']].groupby('company0').sum()/10000
    
    tmp1_0 = tmp1_0.groupby('company0').sum()/10000
    
    tmp1_1 = tmp1_1.groupby('company0').sum()/10000
    
    data_yz = pd.DataFrame({'name':goal0.name},
                           index=[863200, 863201, 863202, 863203, 863204, 863205, 863206, 863207, 863208,863209, 863210, 863211, 863212, 863213]) 

    data_yz['today_new'] = (tmp1_1-tmp1_0).annual + (tmp0_1.groupby('company0').sum()/10000 - tmp0_0.groupby('company0').sum()/10000).single
    data_yz['annual'] = (tmp1_1-tmp1_0).annual
    
    if key == 1:
        data_yz['annual_platform'] = (goal0.all_annual_goal - tmp1_1.annual)/day
    else:
        data_yz['annual_platform'] = (goal1.annual_goal - tmp1_1.annual)/day
    data_yz['ten'] = (tmp1_1-tmp1_0).ten   
    if key == 1:
        data_yz['ten_platform'] = (goal0.all_ten_goal - tmp1_1.ten)/day
    data_yz['today_single'] =  tmp0_1.groupby('company0').sum()/10000 - tmp0_0.groupby('company0').sum()/10000
    data_yz['all_new'] = tmp1_1.annual + tmp0_1.groupby('company0').sum().single/10000
    data_yz['all_annaul'] = tmp1_1['annual']
    if key == 1:
        data_yz['last_annaul'] = last['annual']
        data_yz['annual_year_cent'] = (tmp1_1['annual'] -last['annual'])/last['annual']
        data_yz['annual_goal'] = goal0['annual_goal']
        data_yz['annual_cent'] = tmp1_1.annual/goal0.annual_goal
        fstr=['IF(AND(1,1),"—","—")']
        for n in range(7,20):
            cell = 'N'+str(n)
            fstr.append('=RANK(%s,$%s$7:$%s$19)'%(cell,'N','N'))
        data_yz['annual_rank'] = fstr
        data_yz['all_annual_goal'] = goal0['all_annual_goal']
        data_yz['all_annual_cent'] = tmp1_1.annual/goal0.all_annual_goal
    else:
        data_yz['annual_goal'] = goal1['annual_goal']
        data_yz['annual_cent'] = tmp1_1.annual/goal1.annual_goal
#        data_yz['all_annual_goal'] = goal0['all_annual_goal']
#        data_yz['all_annual_cent'] = tmp1_1.annual/goal0.all_annual_goal
    
    data_yz['all_ten'] = tmp1_1['ten']
    if key == 1:
        data_yz['last_ten'] = last['ten']    
        data_yz['ten_year_cent'] = (tmp1_1['ten']-last['ten'])/last['ten']
        data_yz['ten_goal'] = goal0['ten_goal']
        data_yz['ten_cent'] = tmp1_1.ten/goal0.ten_goal
        fstr=['IF(AND(1,1),"—","—")']
        for n in range(7,20):
            cell = 'V'+str(n)
            fstr.append('=RANK(%s,$%s$7:$%s$19)'%(cell,'V','V'))
        data_yz['ten_rank'] = fstr
        data_yz['all_ten_goal'] = goal0['all_ten_goal']
        data_yz['all_ten_cent'] = tmp1_1.ten/goal0.all_ten_goal
        
    
    data_yz['single'] = tmp0_1.groupby('company0').sum()/10000
    if key == 1:
        data_yz['all_single_goal'] = goal0.all_single_goal
        data_yz['all_single_cent'] = data_yz.single/data_yz.all_single_goal
    print(ti)
    return data_yz,ti[1][1].replace('-','') 

def make_table(values,day,key):
    dic = {2:'bank',1:'post'}
    xlsname = "%s_daliy_%s_performance.xlsx" %(day,dic[key])
#    xlsname = "%s每日业绩.xlsx" %time.strftime('%Y%m%d',time.localtime(time.time()))
#    xlsname2 = "%s每日业绩.xlsx" %(datetime.now()+timedelta(days=-1)).strftime("%Y%m%d")
    workbook = xlsxwriter.Workbook('d:/'+xlsname)
    worksheet = workbook.add_worksheet()    
    merge_format_header = workbook.add_format({'bold': 1,'font_size':20,'font_name':'宋体','align': 'center',
                                               'valign': 'vcenter','font_color':'red','text_wrap':1})
    
    merge_format_col = workbook.add_format({'bold': 1,'font_size':14,'font_name':'宋体','align': 'center',
                                            'valign': 'vcenter','border': 1,'font_color':'black','text_wrap':1})
    merge_format_word = workbook.add_format({'font_size':12,'font_name':'宋体','align': 'center',
                                             'valign': 'vcenter','border': 1,'font_color':'black','text_wrap':1})
    cell_format = workbook.add_format({'font_size':12,'font_name':'宋体','align': 'center',
                                       'valign': 'vcenter','border': 1,'font_color':'black','text_wrap':1})
    cell_format_t2 = workbook.add_format({'font_size':12,'font_name':'宋体','align': 'center',
                                       'valign': 'left','font_color':'black'})
    cell_format1 = workbook.add_format({'font_size':12,'font_name':'宋体','align': 'center',
                                       'valign': 'vcenter','border': 1,'font_color':'black','text_wrap':1})
    cell_format2 = workbook.add_format({'font_size':12,'font_name':'宋体','align': 'center',
                                       'valign': 'vcenter','border': 1,'font_color':'black','text_wrap':1})
    cell_format3 = workbook.add_format({'font_size':12,'font_name':'宋体','align': 'center',
                                       'valign': 'vcenter','border': 1,'font_color':'black','text_wrap':1})
    day_str = '日期：'+day[0:4]+'年'+str(int(day[4:6]))+'月'+str(int(day[6:8]))+'日'
    
    worksheet.set_column('A:U',12)  
    worksheet.set_row(0,39)
    worksheet.set_row(1,26)
    worksheet.set_row(2,18)
    worksheet.set_row(3,30)
    worksheet.set_row(4,47)
    for i in range(5,20):
        worksheet.set_row(i,26)
    data = values.values.T
    worksheet.write_column('B6',data[0],cell_format)
    worksheet.write_column('A6',values.index)
    if key == 1:
        # Merge 3 cells.  邮政报表
        worksheet.merge_range('A1:AB1', '“金铢2019”全省邮政企业中邮保险业绩战报', merge_format_header)
        
        # Merge 3 cells over two rows.
        worksheet.merge_range('C3:H3', '当日', merge_format_col)
        worksheet.merge_range('J3:AB3', '累计', merge_format_col)
        
        worksheet.merge_range('B3:B5', '地区', merge_format_word)
        worksheet.merge_range('C4:C5', '新单总保费', merge_format_word)          #当日
        worksheet.merge_range('D4:G4', '期交保费', merge_format_word)           #当日
        worksheet.merge_range('J4:Q4', '期交保费', merge_format_word)           #一季度累计
        worksheet.merge_range('R4:Y4', '其中：长期期交保费', merge_format_word)   #一季度累计
        worksheet.merge_range('H4:H5', '趸交保费', merge_format_word)
        worksheet.merge_range('I4:I5', '新单总保费', merge_format_word)
        worksheet.merge_range('Z4:AB4', '趸交保费', merge_format_word)
    #    worksheet.write('U4','趸交保费',cell_format)
        title2 = {'B2':day_str,'AA2':'单位：万元'}
        title3 = {'I3':'','D5':'合计','E5':'应达平台','F5':'其中：长期期交','G5':'应达平台',
                  'J5':'合计','K5':'2018年同期','L5':'同比','M5':'一季度计划','N5':'一季度完成率',
                 'O5':'排名','P5':'全年计划','Q5':'全年计划','R5':'合计','S5':'2018年同期','T5':'同比','U5':'一季度计划',
                 'V5':'一季度完成率','W5':'排名','X5':'年计划完成率','Y5':'全年计划完成率','Z5':'合计',
                 'AA5':'全年计划','AB5':'年计划完成率'}
        for k in title3.keys():
            worksheet.write(k,title3[k],cell_format)
        for k in title2.keys():
            worksheet.write(k,title2[k],cell_format_t2)
               
        cell_format1.set_num_format('0.0')
        letter = [chr(i).upper() for i in range(97,123)]
        l=len(letter)
        if data.shape[0]>l:
            for i in range(1,int((data.shape[0]+1)/l+1)):
                for j in range(min(26,1+(data.shape[0]-26*i))):
                    letter.append(letter[i-1]+letter[j])

        
        for num in range(1,7):
            cell = letter[num+1]+str(6)
            worksheet.write_column(cell,data[num],cell_format1)
        for num in range(7,27):
            
            if num not in [10,12,13,15,18,20,21,23,26]:
                cell_format2.set_num_format(0x01) 
    #            print(num+1,len(letter),letter)
                cell = letter[num+1]+str(6)
                worksheet.write_column(cell,data[num],cell_format2)
            elif num in [13,21]:
                for rw in range(6,20):
                    cell = letter[num+1]+str(rw)
                    worksheet.write_formula(cell,data[num][rw-6],cell_format2)
            else:           
                cell_format3.set_num_format('0.0%')
                cell = letter[num+1]+str(6)
                worksheet.write_column(cell,data[num],cell_format3)
        for col in ['A','E','G','I','L','M','P','T','U','X']:        
            worksheet.set_column(col+':'+col, None, None, {'level': 1, 'hidden': True})
    else:                                      
        #银行报表
        worksheet.merge_range('A1:M1', '2019年一季度全省邮储银行中邮保险业绩战报', merge_format_header)
        
        # Merge 3 cells over two rows.
        worksheet.merge_range('C3:G3', '当日', merge_format_col)
        worksheet.merge_range('I3:M3', '一季度累计', merge_format_col)
        
        worksheet.merge_range('B3:B5', '地区', merge_format_word)
        worksheet.merge_range('C4:C5', '新单总保费', merge_format_word)          #当日
        worksheet.merge_range('D4:F4', '期交保费', merge_format_word)           #当日
        worksheet.merge_range('I4:L4', '期交保费', merge_format_word)  

        worksheet.merge_range('G4:G5', '趸交保费', merge_format_word)
        worksheet.merge_range('H4:H5', '新单总保费', merge_format_word)
        worksheet.merge_range('M4:M5', '趸交保费', merge_format_word)
        title2 = {'B2':day_str,'M2':'单位：万元'}
        title3 = {'H3':'','D5':'合计','E5':'应达平台','F5':'其中：长期期交','I5':'合计','J5':'计划',
                  'K5':'完成率','L5':'其中：长期期交保费'}
        for k in title3.keys():
            worksheet.write(k,title3[k],cell_format)
        for k in title2.keys():
            worksheet.write(k,title2[k],cell_format_t2)
               
        cell_format1.set_num_format('0.0')
        letter = [chr(i).upper() for i in range(97,123)]
        l=len(letter)
        if data.shape[0]>l:
            for i in range(1,int((data.shape[0]+1)/l+1)):
                for j in range(min(26,1+(data.shape[0]-26*i))):
                    letter.append(letter[i-1]+letter[j])
        
        for num in range(1,6):
            cell = letter[num+1]+str(6)
            worksheet.write_column(cell,data[num],cell_format1)
        for num in range(6,12):            
            if num ==9:
                cell_format3.set_num_format('0.0%')
                cell = letter[num+1]+str(6)
                worksheet.write_column(cell,data[num],cell_format3)
                
            else:           
                cell_format2.set_num_format(0x01) 
                cell = letter[num+1]+str(6)
                worksheet.write_column(cell,data[num],cell_format2)
        for col in ['A','E','H']:        
            worksheet.set_column(col+':'+col, None, None, {'level': 1, 'hidden': True})
    workbook.close() 
    return 'd:/'+xlsname
def make_inforamtion(data,day,key):
    if key == 2:        
        str_infor={0:'中邮快讯:%s全省邮储银行期交新单保费%s，%s，%s，%s，%s，%s，%s，%s，%s，%s，%s，%s，%s，%s；累计期交新单保费%s（一季度完成率%s)，%s（%s）,%s（%s）,%s（%s）,%s（%s）,%s（%s）,%s（%s）,%s（%s）,%s（%s）,%s（%s）,%s（%s）,%s（%s）,%s（%s）,%s（%s）。'}
        l1 = ['annual']
        l2 = ['all_annaul']
        l3 = ['annual_cent']
        for num in range(1):
            tmp = [str(int(day[4:6]))+'月'+str(int(day[6:8]))+'日']
            sort_tmp1=data.sort_values(l1[num],ascending=False)[['ns',l1[num]]]
            for i in range(14):
                tmp.append(list(sort_tmp1.ns)[i]+"{:.1f}".format(list(sort_tmp1[l1[num]])[i])+'万')
            sort_tmp2=data.sort_values(l2[num],ascending=False)[['ns',l2[num],l3[num]]]
            for i in range(14):
                tmp.append(list(sort_tmp2.ns)[i]+"{:.0f}".format(list(sort_tmp2[l2[num]])[i])+'万')
                tmp.append("{:.0%}".format(list(sort_tmp2[l3[num]])[i]))
#            print(len(tmp))
            str_infor[num] = str_infor[num] %tuple(tmp)
    else:
        str_infor ={0:"中邮快讯1:%s全省中邮期交新单%s，%s，%s，%s，%s，%s，%s，%s，%s，%s，%s，%s，%s，%s; 累计期交新单%s（一季度完成率%s)，%s（%s）,%s（%s）,%s（%s）,%s（%s）,%s（%s）,%s（%s）,%s（%s）,%s（%s）,%s（%s）,%s（%s）,%s（%s）,%s（%s）,%s（%s）。",
        1:"中邮快讯2:%s全省中邮长期期交%s，%s，%s，%s，%s，%s，%s，%s，%s，%s，%s，%s，%s，%s；累计长期期交%s（一季度完成率%s)，%s（%s）,%s（%s）,%s（%s）,%s（%s）,%s（%s）,%s（%s）,%s（%s）,%s（%s）,%s（%s）,%s（%s）,%s（%s）,%s（%s）,%s（%s）。",
        2:"中邮快讯3:%s全省中邮趸交%s，%s，%s，%s，%s，%s，%s，%s，%s，%s，%s，%s，%s，%s;累计趸交%s（年计划完成率%s),%s（%s）,%s（%s）,%s（%s）,%s（%s）,%s（%s）,%s（%s）,%s（%s）,%s（%s）,%s（%s）,%s（%s）,%s（%s）,%s（%s）,%s（%s）。"}
            
    #        data[data.index==863200][['annual','ten','all_annaul','annual_cent','all_ten','ten_cent','single','all_single_cent']]
        
        l1 = ['annual','ten','today_single']
        l2 = ['all_annaul','all_ten','single']
        l3 = ['annual_cent','ten_cent','all_single_cent']
        for num in range(3):
            tmp = [str(int(day[4:6]))+'月'+str(int(day[6:8]))+'日']
            sort_tmp1=data.sort_values(l1[num],ascending=False)[['ns',l1[num]]]
            for i in range(14):
                tmp.append(list(sort_tmp1.ns)[i]+"{:.1f}".format(list(sort_tmp1[l1[num]])[i])+'万')
                sort_tmp2=data.sort_values(l2[num],ascending=False)[['ns',l2[num],l3[num]]]
            for i in range(14):
                tmp.append(list(sort_tmp2.ns)[i]+"{:.0f}".format(list(sort_tmp2[l2[num]])[i])+'万')
                tmp.append("{:.0%}".format(list(sort_tmp2[l3[num]])[i]))
            str_infor[num] = str_infor[num] %tuple(tmp)
    return str_infor


def decode_str(s):
    value, charset = decode_header(s)[0]
    if charset:
        if charset == 'gb2312':
            charset = 'gb18030'
        value = value.decode(charset)
    return value


def get_email_headers(msg):
    headers = {}
    for header in ['From', 'To', 'Cc', 'Subject', 'Date']:
        value = msg.get(header, '')
        if value:
            if header == 'Date':
                headers['Date'] = value
            if header == 'Subject':
                subject = decode_str(value)
                headers['Subject'] = subject
            if header == 'From':
                hdr, addr = parseaddr(value)
                name = decode_str(hdr)
                from_addr = u'%s <%s>' % (name, addr)
                headers['From'] = from_addr
            if header == 'To':
                all_cc = value.split(',')
                to = []
                for x in all_cc:
                    hdr, addr = parseaddr(x)
                    name = decode_str(hdr)
                    to_addr = u'%s <%s>' % (name, addr)
                    to.append(to_addr)
                headers['To'] = ','.join(to)
            if header == 'Cc':
                all_cc = value.split(',')
                cc = []
                for x in all_cc:
                    hdr, addr = parseaddr(x)
                    name = decode_str(hdr)
                    cc_addr = u'%s <%s>' % (name, addr)
                    cc.append(to_addr)
                headers['Cc'] = ','.join(cc)
    return headers


def get_email_content(message,savepath):
    attachments = []
    
    for part in message.walk():
        filename = part.get_filename()
        if filename:
            filename = decode_str(filename)
            data = part.get_payload(decode=True)
            abs_filename = os.path.join(savepath, filename)
            attach = open(abs_filename, 'wb')
            attachments.append(filename)      
            attach.write(data)          
            attach.close()
            if zipfile.is_zipfile(abs_filename):
                os.listdir(os.path.join(savepath,'tmp'))
                for lis in os.listdir(os.path.join(savepath,'tmp')):
#                    print(lis)
                    os.remove(os.path.join(savepath,'tmp')+'/'+lis)
                zipfile.ZipFile(abs_filename).extractall(os.path.join(savepath,'tmp'))               
                l = os.listdir(os.path.join(savepath,'tmp'))
                if len(l)>2:
                    df0=pd.DataFrame()
                    df1=pd.DataFrame() # 0:银行；  1：邮政
                    for xls in l:
                       if xls.startswith('420'):
                           df0=df0.append(read_new_data(os.path.join(savepath,'tmp')+'/'+ xls))
    #                  print(df0.company1)
                       elif xls.startswith('330'):  
                           df1=df1.append(read_insu_data(os.path.join(savepath,'tmp')+'/'+xls))
                    df0['company0']=df0.company1.apply(lambda x: int(str(x)[:-2]))
                    df1['company0']=df1.company1.apply(lambda x: int(str(x)[:-2]))
                    for key in range(1,3):
    #        
                       data,day = compute(df0,df1,key)
                       file=make_table(data,day,key)
#                       print(day)
                       data['ns']=['','宁','锡','徐','常','苏','通','连','淮','盐','扬','镇','泰','宿']
                       str_infor =make_inforamtion(data,day,key)
                       infor =''
                       for k in str_infor.keys():
                           infor += str_infor[k]+'\n'
                       return(infor,file)
                       print(infor)
                       break
#                       return infor,file


if __name__ == '__main__':
#    if os.path.exists('E:/test_email'):    
#        os.remove('E:/test_email')
#        os.mkdir('E:/test_email')        
#    os.chdir('E:/test_email')
    hostname = 'js.postoa.com.cn'
#    user = 'wqm1989@js.postoa.com.cn'
#    passwd = 'qm55201182'
    user = 'wangjunwj@js.postoa.com.cn'
    passwd = 'wj3933660'
    #wqm1989@js.postoa.com.cn,qm55201182
    server = poplib.POP3(hostname, 110)
    server.set_debuglevel(0)
#    print(server.getwelcome())
    server.user(user)
    server.pass_(passwd)
    bot = Bot()
    group=bot.groups()[-1]
    msg_count, msg_size = server.stat()
#    print('message count:', msg_count)
#    print('message size:', msg_size, 'bytes')
    # b'+OK 237 174238271' list()响应的状态/邮件数量/邮件占用的空间大小
    resp, mails, octets = server.list()
    for i in range(1):
        resp, byte_lines, octets = server.retr(msg_count-i)
#        resp, byte_lines, octets = server.retr(i+1)
        # 转码
        str_lines = []
        for x in byte_lines:
            try:
                str_lines.append(x.decode('utf-8'))
            except:
                continue     
        # 拼接邮件内容
        msg_content = '\n'.join(str_lines)
        # 把邮件内容解析为Message对象
        msg = Parser().parsestr(msg_content)
#        os.mkdir('E:/test_email') 
        headers = get_email_headers(msg)
        # print(headers['Subject'],type(headers['Subject']))    (datetime.now()+timedelta(days=-1)).strftime("%Y%m%d") 
        if '日业务数据' in headers['Subject']:                        
#            infor,file = get_email_content(msg,'d:/test_email/')
            infor,file=get_email_content(msg,'d:/test_email/')
        group.send(infor)
        group.send_file(file)
#        print('subject:', headers['Subject'])
#        print('from:', headers['From'])
#        print('to:', headers['To'])
#        if 'cc' in headers:
#            print('cc:', headers['Cc'])
#        print('date:', headers['Date'])
#        print('attachments: ', attachments)
#        print('-----------------------------')

    server.quit()

#            print(xls,tmp.shape)
#    print(new.keys(),insurance.keys())       
#    data = compute_new_data(new)
#    print(data)