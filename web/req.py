import requests, bs4
import re
import uuid
url = 'https://www.amazon.co.jp/s/ref=nb_sb_noss_1?url=search-alias%3Dinstant-video&field-keywords='
keyword = "よりもい"
res = requests.get(url + keyword)
try:
    soup = bs4.BeautifulSoup(res.text, "lxml")
except:
    soup = bs4.BeautifulSoup(res.text, "html5lib")
elems = soup.select('.a-size-medium.s-inline.s-access-title.a-text-normal')
for elem in elems:
    print('{}'.format(elem.getText()))

imgs = soup.find_all('img',src=re.compile('^https://images-'))
for img in imgs:
        print(img['src'])
        r = requests.get(img['src'])
        with open(str('./picture/')+str(uuid.uuid4())+str('.png'),'wb') as file:
                file.write(r.content)

