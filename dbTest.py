#!/usr/bin/python
# -*- coding: utf-8 -*-

import sqlite3
import time

conn = sqlite3.connect('db/douban.db')

cursor = conn.cursor()
cursor.execute("INSERT INTO comment(ID, TIME, MOVIEID, RATING, CONTENT, CREATOR, ADD_TIME) VALUES (NULL, ?, ?, ?, ?, ?, ?)" , ("sss", '2312312', 4, 'i don\'t', '234', '213114'))



# c = conn.cursor()
#
# #c.execute("INSERT INTO comment(ID, TIME, MOVIEID, RATING, CONTENT, CREATOR, ADD_TIME) VALUES (NULL, '2018-1-4', '2312312', 4, 'content', 'user', '213124214')")
# c.execute("INSERT INTO comment(ID, TIME, MOVIEID, RATING, CONTENT, CREATOR, ADD_TIME) VALUES (NULL, '%s', '%s', '%s', '%s', '%s', '%s')" % ("sss", '2312312', 4, '123', '234', '213114'))

conn.commit()
print("Records created successfully")
conn.close()

print("Opened database successfully")