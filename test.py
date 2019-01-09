# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup
import re
from time import sleep
import random
import urllib
import requests
url = "https://douban.com/accounts/login"
formData = {
    "redir": "https://www.douban.com",
    "form_email": "********************",
    "form_password": "********************",
    "login": u'登录',
    'source': 'None',
}

headers = {"User-Agent": "Mozilla/5.0 (Windows NT 6.3; WOW64; Trident/7.0; LCJB; rv:11.0) like Gecko",
           "Referer": "https://douban.com/accounts/login",
           "Host": "accounts.douban.com",
           "Connection": "Keep-Alive",
           "Content-Type": "application/x-www-form-urlencoded"
           }
s = requests.session()
# r_ = s.post(url, data=formData, headers=headers)
# a = r_.text
# soup_ = BeautifulSoup(a, "html.parser")
# captchaAddr = soup_.find('img', id='captcha_image')['src']
# reCaptchaID = r'<input type="hidden" name="captcha-id" value="(.*?)"/'
# captchaID = re.findall(reCaptchaID, a)
# urllib.urlretrieve(captchaAddr, "captcha.jpg")

# captcha = raw_input('please input the captcha:')
# formData['captcha-solution'] = captcha
# formData['captcha-id'] = captchaID

r_ = s.post(url, data=formData, headers=headers)
page_ = r_.text
# print page_
# co = r_.cookies
"""---------------------------------------------------------------------------------"""
number = 0
def process_h3(soup, fp):
    global number
    h3s = soup.findAll("h3")
    for i in h3s:
        aa = i.span.next_siblings
        bb = aa.next().next()
        number += 1
        if number % 100 == 0:
            print number
        if len(bb) == 3:
            fp.write(bb[1].attrs["class"][0][-2:-1])
            fp.write(" ")
            cc = i.next_siblings
            cc.next()
            dd = cc.next().get_text().strip()
            ee = dd.replace('\n', " ")
            fp.write(ee.encode("utf8"))
            fp.write('\n')
def find_next(soup):
    line = soup.findAll("a", {"class", "next"})
    if len(line) == 0:
        return None
    else:
        href = line[0].attrs["href"]
        return target+href
"""---------------------------------------------------------------------------------"""
target = "https://movie.douban.com/subject/25944714/comments"
"""------------------------------------------------------------------------   params"""
movie = s.get(target)   # , cookies=co)
page_movie = movie.text
# print movie.status_code
soupMovie = BeautifulSoup(page_movie)
numb_ = soupMovie.findAll("span", {"class": "fleft"})
total = int(numb_[0].get_text()[3:-1])
print "total:", total,
movieName = soupMovie.find("title").get_text()[:-3]
print movieName
with open(movieName+".txt", 'w') as fp:
    process_h3(soupMovie, fp)
    while True:
        inter = random.gauss(9, 2)
        time = inter if inter > 2.1 else 2.1
        sleep(time)
        next_ = find_next(soupMovie)
        if next_ is None:
            break
        try:
            soupMovie = BeautifulSoup(s.get(next_, timeout=10).text)
            process_h3(soupMovie, fp)
        except:
            sleep(100)
            try:
                soupMovie = BeautifulSoup(s.get(next_, timeout=10).text)
                process_h3(soupMovie, fp)
            except:
                break