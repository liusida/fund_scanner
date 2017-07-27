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

def _test():
    print('TO DO...')
    pass

if (__name__=='main'):
    _test()