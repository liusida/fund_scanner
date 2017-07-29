import unittest
import pymysql.cursors
import fund_scanner.common_tools.database

class TestDatabase(unittest.TestCase):

    def test_get_connection(self):
    	with fund_scanner.common_tools.database.get_connection() as g:
    		self.assertEqual(type(g), pymysql.cursors.DictCursor)

    def test_get_sqlalchemy_engine(self):
    	c = fund_scanner.common_tools.database.get_sqlalchemy_engine()


if __name__ == '__main__':
    unittest.main()