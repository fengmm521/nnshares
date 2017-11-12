#!/usr/bin/env python
#-*- coding: utf-8 -*-
import os,sys
import time
import urllib2
import socket  
import tushare as ts
#将所有Excel文件转为xml文件
reload(sys)
sys.setdefaultencoding( "utf-8" )
dbDir = "sharedata"
txtCoding = 'utf-8'

if not os.path.exists(dbDir):
    os.mkdir(dbDir)

class MyException(Exception):  
        pass 

def isTodayDown(fpth):
    ptime = int(os.path.getctime(fpth))
    loctim = time.localtime(int(ptime))
    numdattmp = int(loctim.tm_year)*10000 + int(loctim.tm_mon)*100 + int(loctim.tm_mday)
    loctim = time.localtime()
    strdate = int(loctim.tm_year)*10000 + int(loctim.tm_mon)*100 + int(loctim.tm_mday)

    if numdattmp == strdate:
        return True
    else:
        return False


def isDownFileOK(datastr):
    tmps = datastr.replace('\r','')
    lines = tmps.split('\n')
    if len(lines[-1]) < 5: 
        lines = lines[:-1]
    if len(lines) > 1:
        return True
    else:
        return False


def downDBFunc(codeid,startdate,enddate,savedir):
    savepth = savedir + os.sep + codeid+'.csv'
    if os.path.exists(savepth) and isTodayDown(savepth):
        print '%s is heave download'%(codeid)
        return True
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

        if isDownFileOK(datatmp):
            if os.path.exists(savepth):
                os.remove(savepth)
            f = open(savepth,'w')
            f.write(datatmp)
            f.close()
            print '下载%s完成,保存在:%s'%(codeid,savepth)
            return True
        else:
            return False
    except urllib2.URLError, e:  
        if isinstance(e.reason, socket.timeout):  
            raise MyException("There was an error: %r" % e)  
        else:  
            # reraise the original error  
            raise
    print '下载%s数据失败...'%(codeid)
    return False

def downDataWithTuShare(tid,pyear):
    tmpth = dbDir + os.sep + str(pyear) + os.sep + '%s.csv'%(codeid)
    dat = ts.get_hist_data(tid) #一次性获取全部日k线数据
    dat.to_csv(tmpth)

def downYearShareDat(pyear):
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

        minyear = pyear * 10000
        maxyear = (pyear + 1) * 10000
        if startDate > minyear and startDate < maxyear:   #获取2016的所有新发行股票ID
            ids.append([tid,startDate])

    ids.sort(key=lambda x:x[1], reverse=False)

    print ids

    yearpth = dbDir + os.sep + str(pyear)
    if not os.path.exists(yearpth):
        os.mkdir(yearpth)

    downErroIDs = []

    startdownday = str(pyear) + '0101'
    enddownday = str(pyear + 1) + '0601' 

    for i in ids:
        tid = i[0]
        print i
        time.sleep(0.05)
        isDown = downDBFunc(tid, startdownday, enddownday,yearpth)
        if not isDown:
            downErroIDs.append(i)

    if downErroIDs:
        print downErroIDs
        print 'redown erro ids with TuShare'
        dcount = len(downErroIDs)
        for i in downErroIDs:
            print 'redwon %s,ddown count is:%d'%(i,dcount)
            downDataWithTuShare(i, pyear)
            dcount -= 1
            print '%s download is ok and sleep 5s...'%(i)
            time.sleep(1)
            print '4'
            time.sleep(1)
            print '3'
            time.sleep(1)
            print '2'
            time.sleep(1)
            print '1'
            time.sleep(1)
    return ids

def main():
    downYearShareDat(2017)

def test():
    print isTodayDown('sharedata/2017/002774.csv')

if __name__ == '__main__':  
    main()
    # test()
