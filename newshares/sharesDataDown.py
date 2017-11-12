#!/usr/bin/env python
#-*- coding: utf-8 -*-
import os,sys
import time
import urllib2
import socket  
#将所有Excel文件转为xml文件
reload(sys)
sys.setdefaultencoding( "utf-8" )
dbDir = "sharedata"
txtCoding = 'utf-8'

if not os.path.exists(dbDir):
    os.mkdir(dbDir)

class MyException(Exception):  
        pass 

def downDBFunc(codeid,startdate,enddate):
    try:  
        urlstr = ""
        print codeid
        if codeid[0] == '6':
            #http://quotes.money.163.com/service/chddata.html?code=1000001&start=20170220&end=20170222
            urlstr = "http://quotes.money.163.com/service/chddata.html?code=0"+ codeid +"&start="+ startdate +"&end=" + enddate
        elif codeid[0] == '3' or codeid[0] == '0':
            urlstr = "http://quotes.money.163.com/service/chddata.html?code=1"+ codeid +"&start="+ startdate +"&end=" + enddate
        print urlstr
        req = urllib2.Request(urlstr)  
        # restr.add_header('Range', 'bytes=0-20')
        resque = urllib2.urlopen(req) 
        datatmp = resque.read()
        savepth = dbDir + os.sep + codeid+'.csv'
        f = open(dbDir + os.sep + codeid+'.csv','w')
        f.write(datatmp)
        f.close()
        print '下载%s完成,保存在:%s'%(codeid,savepth)
        return True
    except urllib2.URLError, e:  
        if isinstance(e.reason, socket.timeout):  
            raise MyException("There was an error: %r" % e)  
        else:  
            # reraise the original error  
            raise
    print '下载%s数据失败...'%(codeid)
    return False
def main():
    f = open('sharelist.csv','r')    #打开文件
    lines = f.readlines()            #按行读取数据，保存一个数组中
    f.close()                        #关闭打开的文件

    print len(lines)                 #输出一共有多少行


    ids = []                         #定义一个空数组，我们要获取的数据之后会保存在这个数组中

    lines = lines[1:]                #去掉第行的标题行数据

    for l in lines:                  #循环处理每一行数据
        tmpl = l.replace('\r','')    #把一行中的'\r'换行符号删除
        tmpl = tmpl.replace('\n','') #把一行中的'\n'回车符号删除

        tmps = tmpl.split(',')       #把一行中的文本按','号截取成一个数据

        tid = tmps[0]                #获取这一行的股票编号
        startDate = int(tmps[15])    #获取这支股票的发行日期,并把原来是字符串的日期文本转换成整数

        if startDate > 20160000 and startDate < 20170000:   #获取2016的所有新发行股票ID
            ids.append([tid,startDate])

    ids.sort(key=lambda x:x[1], reverse=False)

    print ids


    downErroIDs = []

    for i in ids:
        tid = i[0]
        print i
        isDown = downDBFunc(tid, '20160101', '20170401')
        if not isDown:
            downErroIDs.append(i)

if __name__ == '__main__':  
    main()
