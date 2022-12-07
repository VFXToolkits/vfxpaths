import unittest
from vfxpaths import Resolve


class TestResolve(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        print("start test")
    
    @classmethod
    def tearDownClass(cls):
        print("end test")
    
    def test_base(self):
        resolve = Resolve()

