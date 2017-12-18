#!/usr/bin/env python
#-*- coding: utf-8 -*-
import os
import sys
import time
import chardet  #中文编码判断
import urllib2

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

    def getGongGaoTitle(self,browser,lastDate):

        # hurl = 'http://basic.10jqka.com.cn/%s/company.html'%(tid)
        # browser = wdriver
        
        # browser.get(hurl)

        # tabtext = browser.find_element_by_xpath("//div[@id=’manager’ and @stat='company_manager']")
        bardobj = browser.find_element_by_xpath('//*[@id="pub"]')
        # print bardobj.text

        hd = browser.find_element_by_xpath('//*[@id="pub"]/div[1]')

        # print hd.text

        bd = browser.find_element_by_xpath('//*[@id="pub"]/div[2]')
        
        # print bd.text

        #全部公告选项菜单
        allpub = browser.find_element_by_xpath('//*[@id="pub"]/div[2]/div[1]/ul/li[1]/a')                       #董事会菜单

        #业绩公告菜单
        bdjsh = browser.find_element_by_xpath('//*[@id="pub"]/div[2]/div[1]/ul/li[2]/a')                       #监事会菜单
        # print '业绩公告:',bdjsh.text

        #重大事项
        zdsx = browser.find_element_by_xpath('//*[@id="pub"]/div[2]/div[1]/ul/li[3]/a')                       #高管菜单
        # print '重大事项:',zdsx.text

        #股份变动
        gfbd = browser.find_element_by_xpath('//*[@id="pub"]/div[2]/div[1]/ul/li[4]/a')                       #高管菜单
        # print '股份变动:',gfbd.text

        #决议公告
        jygg = browser.find_element_by_xpath('//*[@id="pub"]/div[2]/div[1]/ul/li[5]/a')                       #高管菜单
        # print '决议公告:',jygg.text


        bddshcy = bd.find_element_by_id('pull_all')                    #公告内容

        nowpgcount = 1
        pgcount = -1

        datas = []

        print '开始下载公告内容'

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
            
            for n in range(len(gonggaotexts)):
                # turnto[n].click()                                         #打开成员详情
                h = gonggaotexts[n]                                         #获取公告内容
                try:
                    link = h.find_element_by_class_name('client').get_attribute('href')
                except Exception as e:
                    time.sleep(0.2)
                    link = h.find_element_by_class_name('client').get_attribute('href')
                
                tmpstr = self.conventStrTOUtf8(h.text)
                tmptexts = tmpstr.split('\n')

                if lastDate == tmptexts[0]:
                    break
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
                
                tmpout = tmptexts[0] + '|' + context + '|' + link 
                datas.append(tmpout)               #保存公告内容，有日期也有标题
            if nowpgcount != pgcount:
                time.sleep(0.3)
                nextpageobj.find_element_by_link_text("下一页").click()
                time.sleep(0.5)

        return datas
        

    #获取公司资料
    def companyMsg(self,tid,lastDate = None):

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
        datdic = self.getGongGaoTitle(self.wdriver,lastDate)                                                #获取高管信息

        self.wdriver.quit()

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

    ggdats = sharetool.companyMsg('601933')

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




