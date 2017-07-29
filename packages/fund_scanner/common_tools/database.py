import pymysql.cursors

def get_connection():
    # Connect to the database
    connection = pymysql.connect(host='localhost',
                                 user='funds',
                                 password='funds888',
                                 db='funds',
                                 charset='utf8',
                                 cursorclass=pymysql.cursors.DictCursor)
    return connection
