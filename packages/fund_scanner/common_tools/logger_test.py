import unittest
import fund_scanner.common_tools.logger as logger

class TestLogger(unittest.TestCase):

    @logger.enter_exit_logger
    def test_function(self):
        return



if __name__ == '__main__':
    unittest.main()