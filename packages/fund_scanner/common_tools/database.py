import pymysql.cursors
import sqlalchemy

parameters = {
	'host': 'localhost',
	'user': 'funds',
	'password': 'funds888',
	'db': 'funds',
	'charset': ['utf-8','utf8']
}

def get_connection():
    # Connect to the database
    connection = pymysql.connect(host=parameters['host'],
                                 user=parameters['user'],
                                 password=parameters['password'],
                                 db=parameters['db'],
                                 charset=parameters['charset'][0],
                                 cursorclass=pymysql.cursors.DictCursor)
    return connection

def get_sqlalchemy_engine():
	return sqlalchemy.create_engine("mysql+pymysql://%s:%s@%s/%s?charset=%s"%(
		parameters['user'], parameters['password'], parameters['host'], 
		parameters['db'], parameters['charset'][1]))
