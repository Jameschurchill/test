Date=`date "+%Y-%m-%d %H:%M:%S"`
for i in 192.168.198.20 198.168.198.23 198.168.198.25
do
ping -c4 ${i} >/dev/null 2>&1
if [ $? -ne 0 ];then
   echo "${Date}:it can not ping ${i}"
   continue
fi
done
