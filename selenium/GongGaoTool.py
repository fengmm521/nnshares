#!/usr/bin/env python
#-*- coding: utf-8 -*-
import os
import sys
import time
import chardet  #中文编码判断
import urllib2
import timetool
import hashlib

reload(sys)
sys.setdefaultencoding( "utf-8" )

class GongGaoTool(object):
    """docstring for ClassName"""
    def __init__(self, isCmdMode = True):
        
        self.isCmdMode = isCmdMode
        self.wdriver = None
    #获取高官信息
    # def getManager(wdriver,tid):
    def conventStrTOUtf8(self,oldstr):
        try:
            nstr = oldstr.encode("utf-8")
            return nstr
        except Exception as e:
            print 'nstr do not encode utf-8'
        cnstrtype = chardet.detect(oldstr)['encoding']
        utf8str =  oldstr.decode(cnstrtype).encode('utf-8')
        return utf8str

    def getGongGaoTitle(self,browser,lastMd5):

        # hurl = 'http://basic.10jqka.com.cn/%s/company.html'%(tid)
        # browser = wdriver
        
        # browser.get(hurl)
        browser.implicitly_wait(10)
        # tabtext = browser.find_element_by_xpath("//div[@id=’manager’ and @stat='company_manager']")
        bardobj = browser.find_element_by_xpath('//*[@id="pub"]')
        # print bardobj.text

        hd = browser.find_element_by_xpath('//*[@id="pub"]/div[1]')

        # print hd.text

        bd = browser.find_element_by_xpath('//*[@id="pub"]/div[2]')
        
        # print bd.text

        #全部公告选项菜单
        allpub = browser.find_element_by_xpath('//*[@id="pub"]/div[2]/div[1]/ul/li[1]/a')                       #董事会菜单

        bddshcy = bd.find_element_by_id('pull_all')                    #公告内容

        nowpgcount = 1
        pgcount = -1

        datas = []

        print '开始下载公告内容'

        firstmsgmd5 = ''

        while nowpgcount != pgcount:

            #公告内容://*[@id="pull_all"]/div[1]/dl[1]
            gonggaotexts  = bd.find_elements_by_xpath('//*[@id="pull_all"]/dl')

            if not gonggaotexts:
                gonggaotexts  = bd.find_elements_by_xpath('//*[@id="pull_all"]/div[1]/dl')

            #往期公告页面选择//*[@id="pull_all"]/div[2]/ul
            pageall =  bd.find_element_by_xpath('//*[@id="pull_all"]/div/ul')
            if not pageall:
                pageall =  bd.find_element_by_xpath('//*[@id="pull_all"]/div[2]/ul')

            # print pageall.text
            #最后一页

            pages = bd.find_elements_by_xpath('//*[@id="pull_all"]/div/ul/li')

            pagecountobj = pages[-2]

            pgcount = int(pagecountobj.text)
            # print 'lastpagetext:',pgcount

            nowpgcount = int(pageall.find_element_by_class_name('active').text)
            # print 'current page:',nowpgcount
            #//*[@id="pull_all"]/div[2]/ul/li[10]/a
            nextpageobj = pages[-1]
            # print 'next text:',nextpageobj.text
            frontpageobj = pages[0]
            # print 'front text:',frontpageobj.text

            # print 'ggcount no page:',len(gonggaotexts)

            print 'curren page %d/%d,%d title per page'%(nowpgcount,pgcount,len(gonggaotexts))
            
            isLastDate = False

            for n in range(len(gonggaotexts)):
                # turnto[n].click()                                         #打开成员详情
                h = gonggaotexts[n]                                         #获取公告内容

                try:
                    # linkobj = h.find_element_by_class_name('client')
                    linkobj = h.find_element_by_xpath('//dt/span[2]/a')
                    link = linkobj.get_attribute('href')
                except Exception as e:
                    time.sleep(0.5)
                    #//*[@id="pull_all"]/div[1]/dl[15]/dt/span[2]/a
                    # linkobj = h.find_element_by_class_name('client')
                    linkobj = h.find_element_by_xpath('//dt/span[2]/a')
                    link = linkobj.get_attribute('href')
                
                
                try:
                    tmpstr = self.conventStrTOUtf8(h.text)
                    tmptexts = tmpstr.split('\n')
                    context = tmptexts[1]
                except Exception as e:
                    time.sleep(2)
                    tmpstr = self.conventStrTOUtf8(h.text)
                    tmptexts = tmpstr.split('\n')
                    print tmptexts
                    if tmptexts[0][0] == '2':
                        tmptexts = [tmptexts[0][:10],tmptexts[0][10:]]
                    elif tmptexts[0][2] == ':':
                        tmptexts = [tmptexts[0][:5],tmptexts[0][5:]]
                    context = tmptexts[1]

                if context.find('...') != -1:
                    # print context
                    print 'get text from url'
                    time.sleep(0.1)
                    tmpcontext = self.getUrl(link)
                    time.sleep(0.1)
                    if tmpcontext:
                        titelstart = tmpcontext.find('<title>') + 7
                        endtitle = tmpcontext.find('</title>')
                        context = tmpcontext[titelstart:endtitle]
                    # print context
                if context and context != '':
                    textmd5 = hashlib.md5(context).hexdigest()
                    if lastMd5 == textmd5:
                        isLastDate = True
                        break
                    if firstmsgmd5 == '':
                        firstmsgmd5 = textmd5
                else:
                    textmd5 = 'null'
                tmpout = tmptexts[0] + '|' + context + '|' + link  + '|' +  textmd5 + '|' + timetool.getDateDayWith0() + '|' + str(timetool.timestamp2datetime(int(time.time()))) 
                
                datas.append(tmpout)               #保存公告内容，有日期也有标题
            if isLastDate:
                print 'md5:%s之前数据已存在，只下载最新据数'%(lastMd5)
                break
            if nowpgcount != pgcount:
                time.sleep(0.3)
                nextpageobj.find_element_by_link_text("下一页").click()
                time.sleep(0.5)
        return datas,firstmsgmd5
        

    #获取公司资料
    def companyMsg(self,tid,lastMd5):

        if not self.wdriver:
            if self.isCmdMode:
                print 'used phantomjs'
                import selenium.webdriver.phantomjs.webdriver as wd
                self.wdriver = wd.WebDriver('/usr/local/bin/phantomjs')       #test
                self.wdriver.maximize_window()
            else:
                print 'used chrome'
                import selenium.webdriver.chrome.webdriver as  wd
                self.wdriver = wd.WebDriver('/Users/mage/Documents/tool/cmdtool/chromedriver')       #test
                self.wdriver.maximize_window()

        hurl = 'http://basic.10jqka.com.cn/%s/news.html'%(tid)

    
        self.wdriver.get(hurl)

        #企业高管信息
        datdic = self.getGongGaoTitle(self.wdriver,lastMd5)                                                #获取高管信息
        return datdic

    def getUrl(self,purl):
        try:
            req = urllib2.Request(purl)
            req.add_header('User-agent', 'Mozilla 5.10')
            res = urllib2.urlopen(req)
            html = self.conventStrTOUtf8(res.read())
            return html
        except Exception, e:
            print e
        return None

def main():

    sharetool = GongGaoTool(isCmdMode = False)

    ggdats = sharetool.companyMsg('300103',None)

    for d in ggdats:
        tmpd = d
        print tmpd

    print len(ggdats)
    raw_input('input enter for end.')

    sharetool.wdriver.quit()

def test():
    companytool = GongGaoTool()
    comdic = companytool.companyMsg('600050')
    raw_input('input enter for end.')
    import json 
    tmpstr = json.dumps(comdic,ensure_ascii=False)
    print tmpstr
    f = open('test.txt','w')
    f.write(tmpstr)
    f.close()

#测试
if __name__ == '__main__':
    main()
    # test()




