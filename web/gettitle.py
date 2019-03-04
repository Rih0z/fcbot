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
driver = webdriver.Chrome(chrome_options=options)

# 今は chrome_options= ではなく options=

def getTitleByHint(hsoup):
    hcnt = hsoup.select_one("#rhs_block a")
    if(hcnt is not None):
        htitle = hcnt.getText()
    else:
        htitle = ""
    return htitle

def getTitleByKey(tkeyword):
    turl = 'http://www.google.co.jp/search?hl=jp&gl=JP&num=10&q='
    tres = requests.get(turl + tkeyword)
    tres.raise_for_status()

    try:
        tsoup = bs4.BeautifulSoup(tres.content, "html.parser")
    except:
        tsoup = bs4.BeautifulSoup(tres.content, "html5lib")

    tcnts = tsoup.select("#rhs_block span")
    ttitle = ""
    for tcnt in tcnts:
        tdata = tcnt.getText()
        tp1 = tdata.find("』")
        if(tp1 is not None):
            if(tp1 != -1):
                ttitle = tdata[1:tp1]  
        break
    if (ttitle == ""):
        ttitle = getTitleByHint(tsoup)

    return ttitle
def changeTitle2Urld(ctitle):
    if(ctitle.find("&") != -1):
        ctitle = ctitle.replace('&','%26')
    ctitle = str(furl(ctitle))
    return ctitle

def changeTitle2Urla(ctitle):
    if(ctitle.find("&") != -1):
        ctitle = ctitle.replace('&','＆')
    ctitle = str(furl(ctitle))
    return ctitle

def searchDanime(dtitle):
    durl = "https://anime.dmkt-sp.jp/animestore/sch?searchKey="
    dres = requests.get((durl + changeTitle2Urld(dtitle)))
    dres.raise_for_status()
    dnum = 0
    try:
        dsoup = bs4.BeautifulSoup(dres.content, "html.parser")
    except:
        dsoup = bs4.BeautifulSoup(dres.content, "html5lib")

    dcnt = dsoup.select_one("body > div > div.listHeader.clearfix > p").getText()
    dnum = int(dcnt[0])
    dmes = "dアニメストアで"+dtitle
    if(dnum == 0):
        dmes = dmes + "は見られないよ"
    else:
        dmes = dmes + "は見られるよ.\n関連する動画が"+ dcnt +"見つかったよ"
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
    print(atx+"sss")
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
def searchJW(jmes,jtitle):
    jprovn = jmes
    jprov = ""
    if(jmes == "Netfix"):
        jprov = "nfx" 
    jmes = jmes + "では" + jtitle + "は"
    jurl = "https://www.justwatch.com/jp/検索?q="+jtitle+"&providers="+ jprov   
    #print(jurl)
    jres = requests.get(jurl)
    jres.raise_for_status()
    try:
        jsoup = bs4.BeautifulSoup(jres.content, "html.parser")
    except:
        jsoup = bs4.BeautifulSoup(jres.content, "html5lib")

    jcnts = jsoup.select("body > div.container-fluid.gradient-bg.wrapper > filter-bar > ng-transclude > core-list > div > div > div:nth-child(1) > search-result-entry > div > div:nth-child(2) > div:nth-child(1) > a > span:nth-child(1)")
   # jcnts = jsoup.find_all("span")
    for jcnt in jcnts:
        print(jcnt)
    jmes = jprovn + "で"+jtitle
    return jmes
def main():
    mes = ""
    key = "ゆるゆり"
    print(key+"が入力されたよ")
    title = getTitleByKey(key)
    if(title == ""):
        title = key
    print(title)
    mes = searchDanime(title)
    mes = mes + "\n"
    mes = mes + searchAmazonP(key)
    print(mes)
    searchJW("Netfix",title)
    return

# main関数呼び出し
if __name__ == "__main__":
    main() 
   


