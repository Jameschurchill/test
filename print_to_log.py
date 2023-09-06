doc=open("test1.txt",'w')
print("wo si ni ge",file=doc)
print("ni mei ha",file=doc)

f = open('1.log','a')
c="ni hao"
print(c,file=f)



import sys
sys.stdout = open('1.log', 'a')
print(years)