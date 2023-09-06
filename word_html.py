#coding=utf-8  
   
#�ļ�����  
#BatchConverWords2Html.py  
#˵����  
#������һ���ļ����µ�����.doc/.docx�ļ�תΪ.html�ļ�����Ҫ��װ��Ӧ��win32ģ��  
#���÷�ʽ������Դ����Ŀ¼�����python BatchConverWords2Html.py RootDir  
   
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
                print "********************ERROR: δȡ�ú�׺����"  
           
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