with open("test1.txt",'r+') as file:
     for line in file:
        print("line里面存放的是："+line) # 循环打印文件中每一行内容
       # print(type(line)) # <class 'str'> 类型是字符串