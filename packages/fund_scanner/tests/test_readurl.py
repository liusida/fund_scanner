import env
import unittest
import fund_scanner.readurl as r

class TestReadUrl(unittest.TestCase):
    
    def test_get_content_through_2_method(self):
        url = 'http://fund.eastmoney.com/161713.html'
        method1 = r.read_from_url(url)
        method2 = r.simple_read_from_url(url)
        self.assertNotEqual(method1, '')
        self.assertEqual(method1[50:], method2[50:])

if __name__ == '__main__':
    unittest.main()