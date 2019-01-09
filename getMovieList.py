#!/usr/bin/python
# -*- coding: utf-8 -*-

import urllib
import requests
import json
from storage import DbHelper

index = 0

db_helper = DbHelper.DbHelper()

for index in range(0, 500, 20):
    print(index)

    request_str = "https://movie.douban.com/j/new_search_subjects?sort=T&range=0,10&tags=%E5%A4%A7%E9%99%86,%E5%89%A7%E6%83%85,%E7%94%B5%E5%BD%B1,%E7%BB%8F%E5%85%B8&start=" + ("%d" % index)
    return_data = requests.get(request_str, verify = False)
    json_data = json.loads(return_data.text)
    for json_movie in json_data['data']:
        print('ID : %s  NAME : %s' % (json_movie['id'], json_movie['title']))
        db_helper.insert_movie({'ID':json_movie['id'], 'NAME':json_movie['title']}, "movie_chinese")

db_helper.close_db()

