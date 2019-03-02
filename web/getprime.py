import requests, bs4
#import urllib2
import sys
import re
import uuid
url = 'https://www.amazon.co.jp/s/ref=nb_sb_noss_1?url=search-alias%3Dinstant-video&field-keywords='
keyword = "小林さん ドラゴン"
print(keyword)
res = requests.get(url + keyword)
#html = urllib2.urlopen(url+ keyword)
try:
    soup = bs4.BeautifulSoup(res.text, "html.parser")
except:
    soup = bs4.BeautifulSoup(res.text, "html5lib")

cn = "見つかりませんでした"
cnt =  soup.select_one("#result_0 > div > div > div > div.a-fixed-left-grid-col.a-col-right > div.a-row.a-spacing-small > div > a > h2")
if(type(cnt) is bs4.element.Tag):
    cn = cnt.getText()
else:
    print(cn)
    sys.exit()
print(cn)
#elems = soup.select('.a-size-medium.s-inline.s-access-title.a-text-normal')
#for elem in elems:
#    cn = format(elem.getText())
 #   print(cn)
  #  break

#h2 = soup.find_all('h2',src=re.compile())
tx = ""
tx =  soup.select_one("#result_0 > div > div > div > div.a-fixed-left-grid-col.a-col-right > div:nth-child(2) > div.a-column.a-span7").getText()



if (tx.find("プライム会員特典") != -1):
    print("Amazon Prime")
else:
    print(tx)


