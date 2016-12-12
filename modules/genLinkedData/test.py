
import unittest
from unittest.mock import Mock

class genLinkedDataTest(unittest.TestCase):

    def test_run_new(self):
        self.assertEqual(1,1)

    def test_run_aaaaaaaaaaaa(self):
        print ('jup')

def test():
    suite = unittest.TestLoader().loadTestsFromTestCase(genLinkedDataTest)
    unittest.TextTestRunner(verbosity=2).run(suite)
