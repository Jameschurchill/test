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