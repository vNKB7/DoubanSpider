#!/usr/bin/env python3
# coding=utf-8

from bs4 import BeautifulSoup


class CommentParser:
    __soup = ''
    __movie = None
    __NOT_FOUND = '页面不存在'
    __html_doc = ''


    def __init__(self):
        pass

    def local_load(self, path):
        self.__soup = BeautifulSoup(open(path), 'html.parser')

    def __set_bs_soup(self):

        self.__soup = BeautifulSoup(self.__html_doc, 'html.parser')

    def set_html_doc(self, html_doc):

        self.__html_doc = html_doc


    def __is_404_page(self):

        if self.__html_doc.find(self.__NOT_FOUND) != -1:
            return True

        if len(self.__html_doc) < 500:
            return True

        return False


    def extract_comments(self):
        """
        如果为404或其他出错页面，返回None。
        :return: None|dict
        """

        if self.__html_doc is None:
            return None, "no doc"

        if self.__is_404_page():
            return None, "404"

        # print(self.__html_doc)

        self.__set_bs_soup()

        comments = []

        comments_tag = self.__soup.find(id="comments")
        if comments_tag == None:
            return None, 'no comments'

        comments_list = comments_tag.find_all(class_="comment-item")

        if len(comments_list) == 0:
            return None, 'no comments'

        for comment_items in comments_list:
            try:
                comment = {}
                comment_tag = comment_items.find(class_="comment")
                comment_info_tag = comment_tag.find(class_="comment-info")

                comment["TIME"] = comment_info_tag.find(class_="comment-time ").attrs['title'].strip()
                # print(comment_info_tag)

                comment["RATING"] = comment_info_tag.contents[5].attrs["class"][0][7]
                comment["CREATOR"] = comment_info_tag.a.text.strip()
                comment["CONTENT"] = comment_tag.p.text.strip()

                comments.append(comment)
            except:
                pass

        return comments, 'ok' if len(comments) == 20 else 'no comments'


# cp = CommentParser()
# cp.local_load('F:\code\douban\example.html')
# print(cp.extract_comments())
