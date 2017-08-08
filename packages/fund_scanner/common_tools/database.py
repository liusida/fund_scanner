import pymysql.cursors
import sqlalchemy

parameters = {
    'host': 'localhost',
    'user': 'funds',
    'password': 'funds888',
    'db': 'funds',
    'charset': 'utf8'
}

def get_connection(dbname='funds'):
    # Connect to the database
    connection = pymysql.connect(host=parameters['host'],
                                 user=parameters['user'],
                                 password=parameters['password'],
                                 db=dbname,
                                 charset=parameters['charset'],
                                 cursorclass=pymysql.cursors.DictCursor)
    return connection

def get_sqlalchemy_engine(dbname='funds'):

    return sqlalchemy.create_engine("mysql+pymysql://%s:%s@%s/%s?charset=%s"%(
        parameters['user'], parameters['password'], parameters['host'], 
        dbname, parameters['charset']))
