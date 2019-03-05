#!/usr/bin/env python
# -*- coding: utf-8 -*-
import requests, bs4
#import urllib2
import sys
import re
import uuid
import lxml.html
from furl import furl
reload(sys)
sys.setdefaultencoding('utf-8')


from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import chromedriver_binary

# ブラウザーを起動
options = Options()
options.binary_location = '/Applications/Google Chrome Canary.app/Contents/MacOS/Google Chrome Canary'
options.add_argument('--headless')

jdriver = webdriver.Chrome(chrome_options=options)


def changeTitle2Urld(ctitle):
    ctitle = ctitle.replace('&','＆')
    ctitle = ctitle.replace('＆','%26')
    ctitle = ctitle.replace(' ','　')
    ctitle = ctitle.replace('　','+')
    print(ctitle)
    ctitle = str(furl(ctitle))
    return ctitle

def changeTitle2Urla(ctitle):
    if(ctitle.find("&") != -1):
        ctitle = ctitle.replace('&','＆')
    #ctitle = str(furl(ctitle))
    return ctitle

def getTitleinStr(gtitle):
    tp1 = gtitle.find("』")
    tp2 = gtitle.find("『")
    if(tp1 is not None):
        if(tp1 != -1):
            gtitle = gtitle[tp2+1:tp1]  
    return gtitle
#奇跡も魔法もあるんだよでまどマギをだす関数
def getTitleByHint(hsoup):
    hcnt = hsoup.select_one("#rhs_block a")
    if(hcnt is not None):
        htitle = hcnt.getText()
    else:
        htitle = ""
    return htitle

def getTitleByKey(tkeyword):
    turl = 'http://www.google.co.jp/search?hl=jp&gl=JP&num=10&q=' + changeTitle2Urld(tkeyword)


    tres = requests.get(turl)
    tres.raise_for_status()

    try:
        tsoup = bs4.BeautifulSoup(tres.content, "html.parser")
    except:
        tsoup = bs4.BeautifulSoup(tres.content, "html5lib")

    tcnts = tsoup.select("#rhs_block span")
    ttitle = ""
    for tcnt in tcnts:
        tdata = tcnt.getText()
        ttitle = getTitleinStr(tdata)
        print(tdata + ttitle)
        if(ttitle is not None):
            break
    if (ttitle == ""):
        ttitle = getTitleByHint(tsoup)
    if(ttitle.find("リメイク作品：") != -1 or ttitle.find("著者：") != -1):

        print("changetitle")
        jdriver.get(turl)
        thtml = jdriver.page_source
        try:
            tsoup = bs4.BeautifulSoup(thtml, "html.parser")
        except:
            tsoup = bs4.BeautifulSoup(thtml, "html5lib")

        tcnt = tsoup.select_one("#cnt > div:nth-child(13) > div:nth-child(1) > div:nth-child(2) > div > div:nth-child(3) > div:nth-child(2) > div > div > div > div:nth-child(1) > div > div:nth-child(1) > div > div > div:nth-child(2) > div > span > em:nth-child(1)")
        if (tcnt is not None):
            ttitle = tcnt.getText()

    print("title"+ttitle)
    return ttitle
def searchDanime(dtitle):
    durl = "https://anime.dmkt-sp.jp/animestore/sch?searchKey="
    durl = durl + changeTitle2Urld(dtitle)

    dnum = 0
    jdriver.get(durl)
    dhtml = jdriver.page_source
    try:
        dsoup = bs4.BeautifulSoup(dhtml, "html.parser")
    except:
        dsoup = bs4.BeautifulSoup(dhtml, "html5lib")

    dcnt = dsoup.select_one("body > div > div.listHeader.clearfix > p").getText()
    dnum = int(dcnt[0])
    dmes = "dアニメストアで"
    #ガルパンでバグる対策 だめな処理
    if(dnum == 0 ):
        dmes =  dmes + "は見つけられなかったよ"
    else:
        dmes = dmes +dtitle+ "に関連する動画が"+ dcnt +"\n" + dsoup.select_one("#listContainer > div:nth-child(1) > section > div.itemModuleIn > a > div > h3 > span").getText() +"が見つかったよ"
    return dmes




def searchAmazonP(atitle):
    ames = "AmazonPrimeでは見つけられなかったよ"
    aurl = 'https://www.amazon.co.jp/s/ref=nb_sb_noss_1?url=search-alias%3Dinstant-video&field-keywords='
    atx = ""
    
    ares = requests.get(aurl + changeTitle2Urla(atitle) )
    try:
        asoup = bs4.BeautifulSoup(ares.text, "html.parser")
    except:
        asoup = bs4.BeautifulSoup(ares.text, "html5lib")

    acnt =  asoup.select_one("#result_0 > div > div > div > div.a-fixed-left-grid-col.a-col-right > div.a-row.a-spacing-small > div > a > h2")
    if(type(acnt) is bs4.element.Tag):
        atitle = acnt.getText()
    else:
        return ames
    atx =  asoup.select_one("#result_0 > div > div > div > div.a-fixed-left-grid-col.a-col-right > div:nth-child(2) > div.a-column.a-span7").getText()
    #if(atxs is not None ):
     #   atx = atxs.getText()
    #else:
     #   return ames
    ames = "AmazonPrimeには" + atitle + "があったよ．\n"+ atitle + "は"
    if (atx.find("プライム会員特典") != -1):
        ames= ames +"Prime会員特典だよ"
        return ames
    else:
        ames = ames  + atx + "だよ"
        if(atx == ""):
            ames = "AmazonPrimeで" +  atitle + "は見られないよ"
            return ames
        if(atx.find("￥ 0エピソード レンタル") != -1):
            ames = "\n" + ames + "2話以降は有料かも"
    return ames 

jdriver = webdriver.Chrome(chrome_options=options)

def searchJW(jmes,jtitle):
    jprovn = jmes
    jprov = ""
    if(jmes == "Netfix"):
        jprov = "nfx" 
    if(jmes == "Hulu"):
        jprov = "hlu" 
    if(jmes == "dTV"):
        jprov = "dtv" 
    if(jmes == "U-NEXT"):
        jprov = "unx" 
    if(jmes == "GYAO"):
        jprov = "gyo" 
    jmes = jmes + "では" + jtitle + "は"
    jurl = "https://www.justwatch.com/jp/検索?q="+jtitle+"&providers="+ jprov   
    #print(jurl)
    jdriver.get(jurl)
    jhtml = jdriver.page_source

    try:
        jsoup = bs4.BeautifulSoup(jhtml, "html.parser")
    except:
        jsoup = bs4.BeautifulSoup(jhtml, "html5lib")

    jcnt = jsoup.select_one("body > div.container-fluid.gradient-bg.wrapper > filter-bar > ng-transclude > core-list > div > div > div:nth-child(1) > search-result-entry > div > div:nth-child(2) > div:nth-child(1) > a > span:nth-child(1)")


   # jcnts = jsoup.find_all("span")
    jmes = jprovn + "では"
    if(jcnt is not None):
       jcntn = jcnt.getText()
       jmes = jmes + jcntn + "をみることができるよ"
    else:
       jmes = jmes + "見つけられなかったよ"
    return jmes
def main():
    mes = ""
    key = "バカとテスト"
    print(key+"が入力されたよ")
    title = getTitleByKey(key)
    if(title == ""):
        title = key
    print(title+"について調べたよ")
    mes = searchDanime(title)
    mes = mes + "\n"
    mes = mes + searchAmazonP(key)+ "\n"
    mes = mes + searchJW("Netfix",title)+ "\n"
    mes = mes + searchJW("Hulu",title)+ "\n"
    mes = mes + searchJW("dTV",title)+ "\n"
    mes = mes + searchJW("U-NEXT",title)+ "\n"
    mes = mes + searchJW("GYAO",title)+ "\n"
    print(mes)
    return

# main関数呼び出し
if __name__ == "__main__":
    main() 
   


