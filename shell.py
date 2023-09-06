#!/usr/bin/env python    
# -*- coding: utf-8 -*-   
import os  
if os.system('df -w') !=0:
  print("hello")
  
#获取返回结果 
import os

process = os.popen('ls -l') # return file
output = process.read()
process.close()
print(output)




import os
import subprocess
import sys
import phoenix_utils

phoenix_utils.setPath()

# HBase configuration folder path (where hbase-site.xml reside) for
# HBase/Phoenix client side property override
java_cmd = 'java $HBASE_CLIENT_OPTS -cp ".' + os.pathsep + phoenix_utils.current_dir + os.pathsep + phoenix_utils.phoenix_client_jar_and_xml + \
    '" -Dlog4j.configuration=file:' + \
    os.path.join(phoenix_utils.current_dir, "..", "conf", "log4j.properties") + \
    " org.apache.phoenix.util.PhoenixRuntime " + ' '.join(sys.argv[1:])

subprocess.call(java_cmd, shell=True)



import subprocess
import time
while True:
 retcode = subprocess.call("ping -c4 192.168.198.20",shell=True)
#retcode = subprocess.Popen("ping 192.168.198.20",shell=True)
#retcode.kill()
#retcode.poll()
 time.sleep(10) 
 print("jie zhe ping")
 
 
import subprocess
doc=open("test1.txt",'w')
list=['192.168.198.20','198.168.198.23','198.168.198.25']
print(list)
for i in list:
  retcode = subprocess.call("ping -c4 %s"%(i),shell=True)
#retcode = subprocess.Popen("ping 192.168.198.20",shell=True)
#retcode.kill()
#retcode.poll()
  if retcode !=0:
    print("it can not ping:" +i,file=doc)
    continue