from functools import reduce
l = ['a', 'bc', 'cde', 'defg']
lf = filter(lambda x: len(x) > 2, l)
lm = map(lambda x: x + '_n', l)
lr = reduce(lambda x, y: x + y, l)
a=list(repr(i) for i in l)#等同于a=list(map(lambda x:repr(x),l))
b=",".join('%s' for i in l)
d=','.join(i for i in l)
s=list(('a','bc','cd'))
image ='1.jsp,2.jsp,3.jsp,4.jsp'
image_list = image.strip(',').split(',')#其中Python strip() 方法用于移除字符串头尾指定的字符 split()就是将一个字符串分裂成多个字符串组成的列表
print("a",a)#list转list
#string转list
print(image_list)#['1.jsp', '2.jsp', '3.jsp', '4.jsp']
#filter
print(list(lf)) #['cde', 'defg']
#map
print(list(lm)) #['a_n', 'bc_n', 'cde_n', 'defg_n']
#reduce
print(lr) #abccdedefg
#list转string
print(''.join(l))#abccdedefg
#list转string
print(','.join(l))#a,bc,cde,defg
#list转string
print("b",b)#b: %s,%s,%s,%s
#list转string
print("d:",d)#d: a,bc,cde,defg
#元组转list
print("s:",s)#s: ['a', 'bc', 'cd']


#repr函数是给不带引号的str加引号 给加引号的str加双引号

list1 = ['122', '2333', '3444', '', '', None]
g = list(filter(None, list1))  # 只能过滤空字符和None
print(g)  # ['122', '2333', '3444']