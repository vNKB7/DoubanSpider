#!/usr/bin/env python3
# coding=utf-8

import configparser
import sqlite3
import time

class DbHelper:

    __connection = None

    def __init__(self):
        self.__connect_database()

    def __connect_database(self):
        config = configparser.ConfigParser()
        config.read('config.ini')
        self.__dbPath = config['sqlite']['db_path']
        self.__connection = sqlite3.connect(self.__dbPath)



    def insert_movie(self, movie, table):
        cursor = self.__connection.cursor()
        cursor.execute("INSERT INTO %s(ID,NAME,ADD_TIME) VALUES ('%s', '%s', '%s')" % (table, movie['ID'], movie['NAME'], time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())))
        self.__connection.commit()
        cursor.close()



        # try:
        #     with self.__connection.cursor() as cursor:
        #         cursor.execute("INSERT INTO movie(ID,NAME,ADD_TIME) VALUES ('%s', '%s', '%s')" % (movie['ID'], movie['NAME'], int(time.time())))
        #         self.__connection.commit()
        #     return True
        # finally:
        #     return False

    def insert_comments(self, comments):
        cursor = self.__connection.cursor()
        for comment in comments:
            cursor.execute("INSERT INTO comment(ID, TIME, MOVIEID, RATING, CONTENT, CREATOR, ADD_TIME) VALUES (NULL, ?, ?, ?, ?, ?, ?)" , (comment['TIME'], comment['MOVIEID'], comment['RATING'], transferContent(comment['CONTENT']), comment['CREATOR'], time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())))
        self.__connection.commit()
        cursor.close()

        # with self.__connection.cursor() as cursor:
        #     for comment in comments:
        #         cursor.execute("INSERT INTO comment(ID, TIME, MOVIEID, RATING, CONTENT, CREATOR, ADD_TIME) VALUES (NULL, '%s', '%s', '%s', '%s', '%s', '%s')" % (comment['TIME'], comment['MOVIEID'], comment['RATING'], comment['CONTENT'], comment['CREATOR'], int(time.time())))
        #     self.__connection.commit()
        return True

    def get_movie_id(self, table_name):
        cursor = self.__connection.cursor()
        cursor.execute("select id from %s" % table_name)
        result_set = cursor.fetchall()
        self.__connection.commit()
        cursor.close()
        return [x[0] for x in result_set]


    def close_db(self):
        self.__connection.close()



def transferContent(content):
        if content is None:
            return None
        else:
            string = ""
            for c in content:
                if c == '"':
                    string += '\"'
                elif c == "'":
                    string += "\'"
                elif c == "\\":
                    string += "\\\\"
                else:
                    string += c
            return string
