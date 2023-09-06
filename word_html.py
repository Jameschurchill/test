#coding=utf-8  
   
#文件名：  
#BatchConverWords2Html.py  
#说明：  
#批量将一个文件夹下的所有.doc/.docx文件转为.html文件，需要安装对应的win32模块  
#调用方式：进入源程序目录，命令：python BatchConverWords2Html.py RootDir  
   
from win32com import client as wc  
import os  
word = wc.Dispatch('Word.Application')  
   
def wordsToHtml(dir):  
   
    for path, subdirs, files in os.walk(dir):  
        for wordFile in files:  
            wordFullName = os.path.join(path, wordFile)  
            #print "word:" + wordFullName  
            doc = word.Documents.Open(wordFullName)  
               
            wordFile2 = unicode(wordFile, "gbk")  
            dotIndex = wordFile2.rfind(".")  
            if(dotIndex == -1):  
                print "********************ERROR: 未取得后缀名！"  
           
            fileSuffix = wordFile2[(dotIndex + 1) : ]  
            if(fileSuffix == "doc" or fileSuffix == "docx"):  
                fileName = wordFile2[ : dotIndex]  
                htmlName = fileName + ".html"  
                htmlFullName = os.path.join(unicode(path, "gbk"), htmlName)  
                #htmlFullName = unicode(path, "gbk") + "\\" + htmlName  
                print "generate html:" + htmlFullName  
                doc.SaveAs(htmlFullName, 10)  
                doc.Close()  
       
    word.Quit()  
    print ""  
    print "Finished!"  
       
if __name__ == '__main__':  
    import sys  
    if len(sys.argv) != 2:  
        print "Usage: python funcName.py rootdir"  
        sys.exit(100)  
    wordsToHtml(sys.argv[1])