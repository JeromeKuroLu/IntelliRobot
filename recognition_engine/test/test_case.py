# from .api import TestBkgPattern
import unittest
import os, sys
parentPath = os.path.abspath("..")
if parentPath not in sys.path:
    sys.path.insert(0, parentPath)

if __name__ == '__main__':
    testsuite = unittest.TestLoader().discover(".")
    unittest.TextTestRunner(verbosity=1).run(testsuite)
