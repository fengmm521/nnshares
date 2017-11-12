#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2017-10-25 03:08:47
# @Author  : Your Name (you@example.org)
# @Link    : http://example.org
# @Version : $Id$

import os
import sys

#将所有Excel文件转为xml文件
reload(sys)
sys.setdefaultencoding( "utf-8" )



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


if __name__ == '__main__':  
    main()
    