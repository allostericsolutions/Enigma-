import unittest
from enigma.plugboard import Plugboard

class TestPlugboard(unittest.TestCase):
    def test_swap(self):
        plugboard = Plugboard({'A': 'B', 'B': 'A', 'C': 'D', 'D': 'C'})
        self.assertEqual(plugboard.swap('A'), 'B')
        self.assertEqual(plugboard.swap('B'), 'A')
        self.assertEqual(plugboard.swap('C'), 'D')
        self.assertEqual(plugboard.swap('D'), 'C')
        self.assertEqual(plugboard.swap('E'), 'E')  # No swap

if __name__ == '__main__':
    unittest.main()
