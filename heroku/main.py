from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
)
import os

import requests, bs4
import sys
import re
import urllib

import urllib.request
from urllib.parse import urlparse, parse_qs
from furl import furl
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

options = Options()
options.binary_location = '/app/.apt/usr/bin/google-chrome'

options.add_argument('--headless')
options.add_argument('--disable-gpu')

jdriver = webdriver.Chrome(chrome_options=options)

#jdriver = Chrome(executable_path=driver_path, chrome_options=options)
app = Flask(__name__)

#環境変数取得
YOUR_CHANNEL_ACCESS_TOKEN = os.environ["YOUR_CHANNEL_ACCESS_TOKEN"]
YOUR_CHANNEL_SECRET = os.environ["YOUR_CHANNEL_SECRET"]

line_bot_api = LineBotApi(YOUR_CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(YOUR_CHANNEL_SECRET)


def changeTitle2Urld(ctitle):
    ctitle = ctitle.replace('&','＆')
    ctitle = ctitle.replace('＆','%26')
    ctitle = ctitle.replace(' ','　')
    ctitle = ctitle.replace('　','+')
   # print(ctitle)
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
        if(ttitle is not None):
            break
    if (ttitle == ""):
        ttitle = getTitleByHint(tsoup)

    if(ttitle.find("リメイク作品：") != -1 or ttitle.find("著者：") != -1 or ttitle.find("出版社：") != -1 or ttitle.find("スタジオ：") != -1):

        jdriver.get(turl)
        thtml = jdriver.page_source
        try:
            tsoup = bs4.BeautifulSoup(thtml, "html.parser")
        except:
            tsoup = bs4.BeautifulSoup(thtml, "html5lib")

        tcnt = tsoup.select_one("#cnt > div:nth-child(13) > div:nth-child(1) > div:nth-child(2) > div > div:nth-child(3) > div:nth-child(2) > div > div > div > div:nth-child(1) > div > div:nth-child(1) > div > div > div:nth-child(2) > div > span > em:nth-child(1)")
        if (tcnt is not None):
            ttitle = tcnt.getText()


    if ( ttitle.find("公開日：") != -1):

        jdriver.get(turl)
        thtml = jdriver.page_source
        try:
            tsoup = bs4.BeautifulSoup(thtml, "html.parser")
        except:
            tsoup = bs4.BeautifulSoup(thtml, "html5lib")

        tcnt = tsoup.select_one("#rhs_block > div > div.kp-blk.knowledge-panel.Wnoohf.OJXvsb > div > div.ifM9O > div:nth-child(2) > div.kp-header > div > div.kp-hc > div > div > div.SPZz6b > div.kno-ecr-pt.kno-fb-ctx.gsmt.hNKfZe > span")
        if (tcnt is not None):
            ttitle = tcnt.getText()

    if ( ttitle.find("番組：") != -1):

        jdriver.get(turl)
        thtml = jdriver.page_source
        try:
            tsoup = bs4.BeautifulSoup(thtml, "html.parser")
        except:
            tsoup = bs4.BeautifulSoup(thtml, "html5lib")

        tcnt = tsoup.select_one("#rhs_block > div > div.kp-blk.knowledge-panel.Wnoohf.OJXvsb > div > div.ifM9O > div:nth-child(2) > div.SALvLe.farUxc.mJ2Mod > div > div:nth-child(2) > div > div > span.LrzXr.kno-fv > a")
        if (tcnt is not None):
            ttitle = tcnt.getText()
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
    danit = ""
    #ガルパンでバグる対策 だめな処理
    if(dnum == 0 or dcnt == "42件"):
        dmes =  dmes + "は見つけられなかったよ"
    else:
        dani = dsoup.select_one("#listContainer > div:nth-child(1) > section > div.itemModuleIn > a > div > h3 > span")   
        if(dani is not None):
            danit = dani.getText()
        dmes = dmes +dtitle+ "に関連する動画が"+ dcnt +"\n" 
        if(danit != ""):
            dmes = dmes + danit + "が"
        dmes = dmes + "見つかったよ"
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
    ames = "AmazonPrimeには" + atitle + "があったよ．\n" 
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



def searchHulu(htitle):
    hurl = "https://www.happyon.jp/search?q="
    hurl = hurl + changeTitle2Urld(htitle)

   # print(hurl)
    jdriver.get(hurl)
    dhtml = jdriver.page_source
   # WebDriverWait(jdriver, 30).until(EC.element_to_be_clickable((By.ID, "listContainer")))
    try:
        hsoup = bs4.BeautifulSoup(dhtml, "html.parser")
    except:
        hsoup = bs4.BeautifulSoup(dhtml, "html5lib")

    hcnts = hsoup.find_all("p")
    hlut = ""
    for hcnt in hcnts :
    #    print(hcnt )
        if (hcnt is not None):
            hlut = hcnt.getText();
     #       print(hlut)
            if(hlut.find(htitle) != -1) :
      #          print(htitle + hlut)
                break
            else:
                hlut = ""
    hmes = "Huluで"
    if(hlut == ""):
        hmes =  hmes + "は見つけられなかったよ"
    else:
        hmes = hmes + hlut +"が見つかったよ"
    return hmes




def searchdtv(dvtitle):
    dvurl = "https://pc.video.dmkt-sp.jp/search/increment?words="
    dvurl = dvurl + ((dvtitle))

  #  print(dvurl)
    jdriver.get(dvurl)
    dvhtml = jdriver.page_source
   # WebDriverWait(jdriver, 30).until(EC.element_to_be_clickable((By.ID, "listContainer")))
    try:
        dvsoup = bs4.BeautifulSoup(dvhtml, "html.parser")
    except:
        dvsoup = bs4.BeautifulSoup(dvhtml, "html5lib")

    dvcnts = dvsoup.find_all("strong")
    dvlut = ""
    for dvcnt in dvcnts :
    #    print(dvcnt )
        if (dvcnt is not None):
            dvlut = dvcnt.getText();
   #         print("dtv"+dvlut)
            if(dvtitle[0]== dvlut[0] and dvtitle[1] == dvlut[1] ) :
      #          print(dvtitle + dvlut)
                break
            else:
                dvlut = ""
    dvmes = "dTVで"
    if(dvlut == ""):
        dvmes =  dvmes + "は見つけられなかったよ"
    else:
        dvmes = dvmes + dvlut +"が見つかったよ"
    return dvmes


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
       jmes = jmes +jtitle+"を"+"見つけられなかったよ"
    return jmes
def main():
     return


@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    return 'OK'


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    mes = ""
    key = event.message.text
    title = getTitleByKey(key)
    if(title.find("...") != -1):
        title = getTitleinStr(title)
    #ラーメンで調べるとオックスフォード英和辞典になるので

    if(title == "" or len(title) > 50 or title.find("オックスフォード英語辞典") != -1 or title.find("とは、") != -1 or title.find("リメイク作品：") != -1 or title.find("著者：") != -1 or title.find("出版社：") != -1 or title.find("スタジオ：") != - 1 or title.find("監督：") != -1 or title.find("挿入歌：") != -1  or title.find("挿入歌：") != -1  or title.find("原作：") != -1  or title.find("興行収入：") != -1 or title.find("番組：") != -1   ):
        
        title = key
    mes = title + "について調べたよ\n\n"
    print(mes)
    mes = mes + searchAmazonP(key)+ "\n"

    #searchJW("Netfix",title)+ "\n"
   # mes = mes + searchJW("Netfix",title)+ "\n"
    mes = mes + searchHulu(title)+ "\n"
   # mes = mes + searchJW("U-NEXT",title)+ "\n"
    #mes = mes + searchJW("GYAO",title)+ "\n"
    dmes = ""
    dmes = searchDanime(title)
    if (dmes.find('見つけられなかった') != -1):
        dmes = searchDanime(key)
    mes = mes + dmes + "\n"
    dmes = ""
    dmes = searchdtv(key)
    mes = mes + dmes 
    #mes = mes + searchJW("dTV",title)
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text = mes)
    )

if __name__ == "__main__":
#    app.run()
    port = int(os.getenv("PORT", 5000))
    app.run(host="0.0.0.0", port=port)

