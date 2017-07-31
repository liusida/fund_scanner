
import unittest
import fund_scanner.business.grab_data as target

from pprint import PrettyPrinter

import fund_scanner.common_tools.database as db

pp = PrettyPrinter(indent=4)

class TestGetDataFromWebsite(unittest.TestCase):

    def test_get_funds(self):
        funds = target.get_funds(['512880', '000501', '180028', '540006'])
        pp.pprint(funds)
        self.assertEqual(funds['512880']['funds_name_full'], '国泰中证全指证券公司ETF')
        self.assertEqual(funds['512880']['funds_type'], 'ETF-场内')
        self.assertEqual(funds['000501']['funds_type'], '固定收益')
        self.assertEqual(funds['180028']['funds_type'], '保本型')
        self.assertEqual(funds['540006']['funds_type'], '股票型')

    def test_write_funds_to_database(self):
        funds = target.get_funds(['002480'])
        self.assertTrue(funds is not None)

        #pp.pprint(funds)
        target.write_funds_to_database(funds)
        with db.get_connection() as cursor:
            for funds_code, each_fund in funds.items():
                sql = 'select * from `funds` where `funds_code`=%s;'
                cursor.execute(sql, funds_code)
                rs = cursor.fetchall()
                self.assertEqual(len(rs), 1)
                self.assertEqual(rs[0]['funds_code'], '002480')

                funds_id = rs[0]['funds_id']
                sql = 'select * from `funds_update` where `funds_id`=%s;'
                cursor.execute(sql, funds_id)
                rs = cursor.fetchall()
                #pp.pprint(rs)
                self.assertEqual(len(rs), 1)
                self.assertEqual(rs[0]['funds_amount'], float(each_fund['funds_amount']))

    def test_update_funds(self):
        target.update_funds(['000049'])
        with db.get_connection() as cursor:
            sql = 'SELECT a.`update_time` as a_time, b.`update_time` as b_time FROM `funds` a LEFT JOIN `funds_update` b ON a.`funds_id`=b.`funds_id` WHERE a.`funds_code`=%s'
            cursor.execute(sql, ('000049',))
            rs = cursor.fetchall()
            self.assertEqual(len(rs), 1)
            self.assertEqual(rs[0]['a_time'],rs[0]['b_time'])

if __name__ == '__main__':
    unittest.main()