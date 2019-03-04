#!/usr/bin/env python
# -*- coding: utf-8 -*-
import requests, bs4
#import urllib2
import sys
import re
import uuid
import lxml.html

reload(sys)
sys.setdefaultencoding('utf-8')
turl = 'http://www.google.co.jp/search?hl=jp&gl=JP&num=10&q='

def getTitleByHint(hsoup):
    hcnt = hsoup.select_one("#rhs_block a")
    htitle = hcnt.getText()
    return htitle

def getTitleByKey(tkeyword):
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

def main():
    title = getTitleByKey("奇跡も魔法もあるんだよ")
    print(title)
    return

# main関数呼び出し
if __name__ == "__main__":
    main() 
   


