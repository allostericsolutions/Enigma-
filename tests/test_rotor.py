
import unittest
from enigma.rotor import Rotor

class TestRotor(unittest.TestCase):
    def test_forward(self):
        rotor = Rotor("EKMFLGDQVZNTOWYHXUSPAIBRCJ", 16)
        rotor.set_position(0)
        self.assertEqual(rotor.forward('A'), 'E')
        self.assertEqual(rotor.forward('B'), 'K')

    def test_backward(self):
        rotor = Rotor("EKMFLGDQVZNTOWYHXUSPAIBRCJ", 16)
        rotor.set_position(0)
        self.assertEqual(rotor.backward('E'), 'A')
        self.assertEqual(rotor.backward('K'), 'B')

    def test_rotate(self):
        rotor = Rotor("EKMFLGDQVZNTOWYHXUSPAIBRCJ", 16)
        rotor.set_position(0)
        self.assertFalse(rotor.rotate())
        rotor.set_position(15)
        self.assertTrue(rotor.rotate())

if __name__ == '__main__':
    unittest.main()
