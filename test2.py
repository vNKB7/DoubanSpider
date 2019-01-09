from storage import DbHelper


db_helper = DbHelper.DbHelper()
comments = [{'MOVIEID':"233"}]
db_helper.insert_comments(comments)
db_helper.close_db()