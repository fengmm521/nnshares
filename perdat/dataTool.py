#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2017-10-25 03:08:47
# @Author  : Your Name (you@example.org)
# @Link    : http://example.org
# @Version : $Id$

import os
import codecs
import sys
import time
import shutil 


import numpy
import json

#将所有Excel文件转为xml文件
reload(sys)
sys.setdefaultencoding( "utf-8" )

def cur_file_dir():
    #获取脚本路径
    path = sys.path[0]
    #判断为脚本文件还是py2exe编译后的文件，如果是脚本文件，则返回的是脚本的目录，如果是py2exe编译后的文件，则返回的是编译后的文件路径
    if os.path.isdir(path):
        return path
    elif os.path.isfile(path):
        return os.path.dirname(path)

#获取父目录
def GetParentPath(strPath):
    if not strPath:
        return None;
    lsPath = os.path.split(strPath);
    if lsPath[1]:
        return lsPath[0];
    lsPath = os.path.split(lsPath[0]);
    return lsPath[0];

#获取所有界面的json文件列表
def getAllExtFile(path,fromatx = ".txt"):
    jsondir = path
    jsonfilelist = []
    for root, _dirs, files in os.walk(jsondir):
        for filex in files:          
            #print filex
            name,text = os.path.splitext(filex)
            if cmp(text,fromatx) == 0:
                jsonArr = []
                rootdir = path
                dirx = root[len(rootdir):]
                pathName = dirx +os.sep + filex
                jsonArr.append(pathName)
                (newPath,_name) = os.path.split(pathName)
                jsonArr.append(newPath)
                jsonArr.append(name)
                jsonfilelist.append(jsonArr)
    return jsonfilelist



def getAllQFQDataID():
    fs = getAllExtFile('qfqdata','.csv')
    print fs[0]
    ids = []
    for d in fs:
        ids.append(d[2])
    return ids


def deSoftMaxFromLable(lab):
    pass

def softMaxLable(mindown,maxup):
    #true table
    tb ='-19,-17,-15,-13,-11,-9,-7,-5,-3,-2,-1,1,2,3,5,7,9,11,13,15,17,19'
    truetables = tb.split(',')
    num = len(truetables) + 1  #23x23=529
    alllabnum = num*num
    labs = [0]*alllabnum
    # print labs
    maxIndex = num - 1
    minIndex = 0
    for n in range(num - 1):
        tmpf = float(truetables[n])
        if minIndex == 0 and mindown < tmpf:
            minIndex = n
        if maxIndex == num - 1 and maxup < tmpf:
            maxIndex = n 
    maxIndex += 1
    minIndex += 1
    labs[minIndex*maxIndex] = 1
    return labs

def getPerdatLable(onedat,labDayCount = 7):
    ldats = onedat[1]
    if not ldats:
        return None
    # print ldats
    maxclose = 0.0
    minclose = 99999.0
    for d in ldats:
        if d[1] > maxclose:
            maxclose = d[1]
        if d[2] < minclose:
            minclose = d[2]
    lastclose = onedat[0][-1][3]
    # print lastclose

    maxup = (maxclose - lastclose)/lastclose
    mindown = (minclose - lastclose)/lastclose

    labdat = softMaxLable(mindown, maxup)

    newperdat = []

    perdat = onedat[0]
    for d in perdat:
        tmp0 = (d[0] - lastclose)/(3*lastclose)
        if tmp0 >= 1.0:
            tmp0 = 1.0
        tmp1 = (d[1] - lastclose)/(3*lastclose)
        if tmp1 >= 1.0:
            tmp1 = 1.0
        tmp2 = (d[2] - lastclose)/(3*lastclose)
        if tmp2 >= 1.0:
            tmp2 = 1.0
        tmp3 = (d[3] - lastclose)/(3*lastclose)
        if tmp3 >= 1.0:
            tmp3 = 1.0
        tmpone = [tmp0,tmp1,tmp2,tmp3,d[4]]
        newperdat.append(tmpone)
    outdats = []
    outdats.append(newperdat)
    outdats.append(labdat)
    return outdats


def saveListToFileWithJson(tpath,dats):
    savetxt = json.dumps(dats)
    f = open(tpath,'w')
    f.write(savetxt)
    f.close()

def loadListFromFileWithJson(tpth):
    f = open(tpth,'r')
    jsontxt = f.read()
    f.close()
    outlist = json.loads(jsontxt)
    return outlist

def createNNCOuntDayTmpData(tid,pDay = 100,labDayCount = 7):
    f = open('qfqdata/' + tid + '.csv','r')
    tmpd = f.readlines()[1:]
    f.close()

    #code,time,open,high,low,close,volume,turn,trate
    perdata = []   #per data is 100 lines,data from after to now
    lcount = len(tmpd)
    for n in range(len(tmpd)):
        if n+pDay < lcount:
            onedat = []
            ppdat = []
            for ln in range(n,n+pDay):
                tmpl = tmpd[ln]
                tmpl = tmpl.replace('\r','')
                tmpl = tmpl.replace('\n','')
                ds = tmpl.split(',')
                ppdat.append([float(ds[2]),float(ds[3]),float(ds[4]),float(ds[5]),float(ds[8])])
            onedat.append(ppdat)
            labdat = []
            if n + pDay + labDayCount < lcount:
                for ln2 in range(n+pDay,n+pDay+labDayCount):
                    tmpl2 = tmpd[ln2]
                    tmpl2 = tmpl2.replace('\r','')
                    tmpl2 = tmpl2.replace('\n','')
                    ds2 = tmpl2.split(',')
                    labdat.append([float(ds2[2]),float(ds2[3]),float(ds2[4]),float(ds2[5]),float(ds2[8])])
            onedat.append(labdat)
            perdata.append(onedat)
    newperdata = []
    datlong = len(perdata)
    index = 0
    for d in perdata:
        tmpnew = getPerdatLable(d)
        if tmpnew:
            newperdata.append(tmpnew) 

    dirpath = '/media/mage/000FBF7E00093795/linuxfiles/perdata/' + 'tmp' + str(pDay) + '_' + str(labDayCount)
    if not os.path.exists(dirpath):
        os.mkdir(dirpath)
    savepath = dirpath + os.sep + tid + '.txt'
    saveListToFileWithJson(savepath, newperdata)

def createNN100DayTmpData(tid,labDay = 7):
    return createNNCOuntDayTmpData(tid,100,labDay)


def createNN30DayTmpData(tid,labDay = 3):
    return createNNCOuntDayTmpData(tid,30,3)

def createNN10DayTmpData(tid,labDay = 3):
    return createNNCOuntDayTmpData(tid,10,3)

def main():
    ids = getAllQFQDataID()
    index = 0
    for t in ids:
        index += 1
        print index,t
        createNN100DayTmpData(t)
        # createNN30DayTmpData(t)
        # createNN10DayTmpData(t)

def test():
    # a = range(100,103)
    # print a
    # SoftMaxLable(-5.1,6.3)
    # os.mkdir('aaa')
    aaa = [0]*10
    bbb = []
    bbb.append(aaa)
    bbb.append([5,5,5,5,5,5,5])
    saveListToFileWithJson('aaa.txt', bbb)
    rlist = loadListFromFileWithJson('aaa.txt')
    print rlist
if __name__ == '__main__':  
    main()
    # test()
    