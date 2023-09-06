import re
line=['hello','train','trainsll','hehe']
for i in  line:
    match=re.findall('^trai.*',i)
    if match != []:
        print(match[0])