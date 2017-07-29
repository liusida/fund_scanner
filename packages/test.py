import unittest

suite = unittest.TestLoader().discover('.', pattern = "*_test.py")
unittest.TextTestRunner(verbosity=2).run(suite)