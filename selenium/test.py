#!/usr/bin/env python
#-*- coding: utf-8 -*-
import os
import sys
import time

import selenium.webdriver.chrome.webdriver as  wd

#获取高官信息
# def getManager(wdriver,tid):
def getManager(browser):

    # hurl = 'http://basic.10jqka.com.cn/%s/company.html'%(tid)
    # browser = wdriver
    
    # browser.get(hurl)

    datas = {}

    # tabtext = browser.find_element_by_xpath("//div[@id=’manager’ and @stat='company_manager']")
    manger = browser.find_element_by_id('manager')
    hd = manger.find_element_by_class_name('hd')
    bd = manger.find_element_by_class_name('bd')

    print hd.text
    # browser.find_element_by_id('kw').send_keys('selenium')
    # browser.find_element_by_id('su').click()
    bddsh = bd.find_element_by_name('ml_001')                       #董事会菜单

    print '董事会菜单:',bddsh.text

    bdjsh = bd.find_element_by_name('ml_002')                       #监事会菜单

    print '监事会菜单:',bdjsh.text

    bdgg = bd.find_element_by_name('ml_003')                        #高管菜单

    print '高管菜单:',bdgg.text
    bddshcy = bd.find_element_by_id('ml_001')                       #董事会成员列表,注意这个是by_id

    print '董事会成员',bddshcy.text
    turnto = bddshcy.find_elements_by_class_name('turnto')         #成员名列表
    hidds = bddshcy.find_elements_by_class_name('person_table')     #发现person列表数组

    dattmps = []
    for n in range(len(turnto)):
        turnto[n].click()                                          #打开成员详情
        h = hidds[n]                                                #获取详情内容
        clo = h.find_element_by_class_name('close')                 #关闭按钮
        dattmps.append(h.text)                                      #保存详情
        clo.click()                                                 #关闭当前详情

    datas['dsh'] = dattmps

    time.sleep(0.1)

    bdjsh.click()               #点击打开监事会列表

    time.sleep(0.1)

    bdjshcy = bd.find_element_by_id('ml_002')                   #监事会成员列表,by_id

    print '监事会成员:',bdjshcy.text
    turnto = bdjshcy.find_elements_by_class_name('turnto')         #成员名列表
    hidds = bdjshcy.find_elements_by_class_name('person_table')     #发现person列表数组

    dattmps = []
    for n in range(len(turnto)):
        turnto[n].click()                                          #打开成员详情
        h = hidds[n]                                                #获取详情内容
        clo = h.find_element_by_class_name('close')                 #关闭按钮
        dattmps.append(h.text)                                      #保存详情
        clo.click()                                                 #关闭当前详情

    datas['jsh'] = dattmps

    bdgg.click()                #打开高管列表
    time.sleep(0.1)

    ggcy = bd.find_element_by_id('ml_003')                  #高管列表,by_id

    print '高管成员:',ggcy.text
    turnto = ggcy.find_elements_by_class_name('turnto')         #成员名列表
    hidds = ggcy.find_elements_by_class_name('person_table')     #发现person列表数组

    dattmps = []
    for n in range(len(turnto)):
        turnto[n].click()                                          #打开成员详情
        h = hidds[n]                                                #获取详情内容
        clo = h.find_element_by_class_name('close')                 #关闭按钮
        dattmps.append(h.text)                                      #保存详情
        clo.click()                                                 #关闭当前详情

    datas['gg'] = dattmps

    return datas
    

#获取企业详细信息
# def getCompanyMsg(wdriver,tid):
def getCompanyMsg(browser):
    # hurl = 'http://basic.10jqka.com.cn/%s/company.html'%(tid)

    # datas = {}

    # browser = wdriver
    
    # browser.get(hurl)

    company = browser.find_element_by_id('detail')
    # hd = company.find_element_by_class_name('hd')
    bd = company.find_element_by_class_name('bd')

    # print hd.text
    # browser.find_element_by_id('kw').send_keys('selenium')
    # browser.find_element_by_id('su').click()
    bdtitle = bd.find_element_by_class_name('m_table')                       #公司名称，所属地，主页,曾用名

    outstr =  bdtitle.text + '\n'


    othmsg = bd.find_element_by_class_name('ggintro')                      #ggintro

    # print othmsg.text
    outstr += othmsg.text

    return outstr


#获取企业发行相关
# def getPublishMsg(wdriver,tid):
def getPublishMsg(browser):
    # hurl = 'http://basic.10jqka.com.cn/%s/company.html'%(tid)

    # # datas = {}

    # browser = wdriver
    
    # browser.get(hurl)

    company = browser.find_element_by_id('publish')
    # hd = company.find_element_by_class_name('hd')
    bd = company.find_element_by_class_name('bd')

    morebtn = bd.find_element_by_class_name('more')
    morebtn.click()

    bdtitle = bd.find_element_by_class_name('m_table')                       #公司名称，所属地，主页,曾用名

    outmsg = bdtitle.text

    return outmsg

# def getSharesCompanys(wdriver,tid):

def getSharesCompanys(browser):
    # hurl = 'http://basic.10jqka.com.cn/%s/company.html'%(tid)

    # browser = wdriver
    
    # browser.get(hurl)

    share = browser.find_element_by_id('share')

    pagescroll = share.find_element_by_class_name('pagescroll')

    business = share.find_element_by_class_name('business')
    

    mcap = business.find_element_by_class_name('m_cap')

    listhand = business.find_element_by_xpath('//*[@id="ckg_table"]/thead')


    outstr = mcap.text + '\n' + listhand.text + '\n'
    # print outstr  //*[@id="ckg_table"]/tbody
    tmpstrs = pagescroll.text.split('\n')
    for p in tmpstrs:
        ckgkey = 'ckg_table_fy' + p
        pagebtn = pagescroll.find_element_by_id(ckgkey).find_element_by_link_text(p)
        pagebtn.click()
        time.sleep(0.3)
        companys = business.find_element_by_xpath('//*[@id="ckg_table"]/tbody')
        outstr += companys.text + '\n'

    return outstr


#获取公司资料
def companyMsg(tid):
    wdriver = wd.WebDriver('/Users/mage/Documents/tool/cmdtool/chromedriver')       #test

    hurl = 'http://basic.10jqka.com.cn/%s/company.html'%(tid)

    wdriver.get(hurl)

    outdic = {} 

    #公司详情
    companymsg = getCompanyMsg(wdriver)
    # print companymsg
    outdic['xxqk'] = companymsg

    #企业高管信息
    datdic = getManager(wdriver)                                                #获取高管信息
    outdic['ggjs'] = datdic

    #获取发行信息
    fxmsg = getPublishMsg(wdriver)
    # print fxmsg
    outdic['fxxg'] = fxmsg

    #获取参股企业
    outmsg = getSharesCompanys(wdriver)
    # print outmsg
    outdic['cgkggs'] = outmsg

    return outdic

def main():

    wdriver = wd.WebDriver('/Users/mage/Documents/tool/cmdtool/chromedriver')       #test
    # browser = webdriver.phantomjs()

    #企业高管信息
    # datdic = getManager(wdriver,tid)                                                #获取高管信息

    #公司详情
    # companymsg = getCompanyMsg(wdriver, '603289')
    # print companymsg

    #获取发行信息
    # outmsg = getPublishMsg(wdriver, '603289')
    # print outmsg

    #获取参股企业
    # outmsg = getSharesCompanys(wdriver, '600050')
    # print outmsg

    raw_input('input enter for end.')

    wdriver.quit()

def test():
    comdic = companyMsg('600050')
    print comdic

#测试
if __name__ == '__main__':
    # main()
    test()




