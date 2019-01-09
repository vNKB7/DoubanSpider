#!/usr/bin/env python3
# coding=utf-8


import configparser
from login import CookiesHelper
from page_parser import CommentParser
from storage import DbHelper
import random
import constants
import requests
import time

def delay(min_second, max_second):
    time.sleep(random.randrange(min_second, max_second))

# 读取配置文件信息
accountConfig = configparser.ConfigParser()
accountConfig.read('account.ini')

# 获取模拟登录后的cookies
cookie_helper = CookiesHelper.CookiesHelper(
    accountConfig['douban']['user'],
    accountConfig['douban']['password']
)

cookies = cookie_helper.get_cookies()
print(cookies)


# 实例化爬虫类和数据库连接工具类
comment_parser = CommentParser.CommentParser()
db_helper = DbHelper.DbHelper()


movieList = db_helper.get_movie_id('movie')
# movieList = ['']

count = 17

for i in range(17, len(movieList)):
# for movieId in movieList:
    movieId = movieList[i]
    print('movie id = %s  %d / %d' % (movieId, count, len(movieList)))
    count += 1

    posCt = 0
    negCt = 0


    # 因为负面评论一般比正面评论少，为了正负样例均衡，先爬负面的
    while True:
        headers = {'User-Agent': random.choice(constants.USER_AGENT)}

        request_str = "https://movie.douban.com/subject/" + ("%s" % movieId) + "/comments?start=" + ("%d" % negCt) + "&limit=20&sort=new_score&status=P&percent_type=l"

        # 获取豆瓣页面(API)数据
        r = requests.get(
            request_str,
            headers=headers,
            cookies=cookies
        )
        r.encoding = 'utf-8'

        #print(request_str)

        # 提取豆瓣数据
        comment_parser.set_html_doc(r.text)

        comments, state = comment_parser.extract_comments()

        if state == 'no comments':
            print('no comments')
            break
        elif state != 'ok':
            print('not ok')
            delay(constants.DELAY_MIN_SECOND, constants.DELAY_MAX_SECOND)
            exit(-1)
            continue

        # 豆瓣数据有效，写入数据库

        for comment in comments:
            comment['MOVIEID'] = movieId

        # for comment in comments:
        #     print(comment['MOVIEID'], comment["TIME"], comment["RATING"], comment["CREATOR"], comment["CONTENT"])


        db_helper.insert_comments(comments)

        delay(constants.DELAY_MIN_SECOND, constants.DELAY_MAX_SECOND)

        negCt += 20

        #print("neg movie : %s   index : %d" % (movieId, negCt))

    delay(10, 40)

    while posCt < negCt * 2:
        headers = {'User-Agent': random.choice(constants.USER_AGENT)}

        request_str = "https://movie.douban.com/subject/" + ("%s" % movieId) + "/comments?start=" + ("%d" % posCt) + "&limit=20&sort=new_score&status=P&percent_type=h"

        # 获取豆瓣页面(API)数据
        r = requests.get(
            request_str,
            headers=headers,
            cookies=cookies
        )
        r.encoding = 'utf-8'

        #print(request_str)

        # 提取豆瓣数据
        comment_parser.set_html_doc(r.text)

        comments, state = comment_parser.extract_comments()

        if state == 'no comments':
            print('no comments')
            break
        elif state != 'ok':
            print('not ok')
            delay(constants.DELAY_MIN_SECOND, constants.DELAY_MAX_SECOND)
            exit(-1)
            continue

        # 豆瓣数据有效，写入数据库

        for comment in comments:
            comment['MOVIEID'] = movieId

        # for comment in comments:
        #     print(comment['MOVIEID'], comment["TIME"], comment["RATING"], comment["CREATOR"], comment["CONTENT"])

        db_helper.insert_comments(comments)

        delay(constants.DELAY_MIN_SECOND, constants.DELAY_MAX_SECOND)

        posCt += 20

        #print("pos movie : %s   index : %d" % (movieId, posCt))

    print("movie : %s   pos : %d   neg : %d" % (movieId, posCt, negCt))
    delay(60, 300)

db_helper.close_db()