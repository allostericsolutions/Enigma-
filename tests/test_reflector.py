import unittest
from enigma.reflector import Reflector

class TestReflector(unittest.TestCase):
    def test_reflect(self):
        reflector = Reflector("YRUHQSLDPXNGOKMIEBFZCWVJAT")
        self.assertEqual(reflector.reflect('A'), 'Y')
        self.assertEqual(reflector.reflect('B'), 'R')
        self.assertEqual(reflector.reflect('C'), 'U')

if __name__ == '__main__':
    unittest.main()
