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

class MyException(Exception):  
        pass 

def getFront60Dat(codeid,datcount = 60):

    outlist = []

    tmpth = dbDir + os.sep + '%s.csv'%(codeid)
    if not os.path.exists(tmpth):
        print '股票%s不存在，查看是否下地了这支股票的数据'%(tmpth)
        return None

    f = open(tmpth,'r')
    lines = f.readlines()
    f.close()

    lines = lines[1:]

    for l in lines:
        tmpl = l.replace('\r','')
        tmpl = tmpl.replace('\n','')
        tmps = tmpl.split(',')
        outlist.append(tmps)


    outlist.sort(key=lambda x:x[0], reverse=False)

    k = 0
    for k in range(len(outlist)):
        if outlist[k][2][0] != 'N':
            k += 1
        else:
            print 'tid:%s,new k is:%d'%(codeid,k)
            break
    outlist = outlist[k:k+datcount]


    return outlist





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


    datdic = {}

    for i in ids:
        tid = i[0]
        print i
        fdat = getFront60Dat(tid,60)
        if fdat:
            datdic[tid] = fdat


if __name__ == '__main__':  
    main()
