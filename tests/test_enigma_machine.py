import unittest
from enigma.rotor import Rotor
from enigma.reflector import Reflector
from enigma.plugboard import Plugboard
from enigma.enigma_machine import EnigmaMachine

class TestEnigmaMachine(unittest.TestCase):
    def setUp(self):
        # Configuración inicial de los rotores y plugboard
        self.rotor_I = Rotor("EKMFLGDQVZNTOWYHXUSPAIBRCJ", 16)
        self.rotor_II = Rotor("AJDKSIRUXBLHWTMCQGZNPYFVOE", 4)
        self.rotor_III = Rotor("BDFHJLCPRTXVZNYEIWGAKMUSQO", 21)
        self.reflector_B = Reflector("YRUHQSLDPXNGOKMIEBFZCWVJAT")
        self.plugboard = Plugboard({'A': 'B', 'B': 'A', 'C': 'D', 'D': 'C'})
        self.enigma = EnigmaMachine([self.rotor_I, self.rotor_II, self.rotor_III], self.reflector_B, self.plugboard)

    def test_encrypt_decrypt(self):
        # Configuración de la posición inicial de los rotores
        self.rotor_I.set_position(0)
        self.rotor_II.set_position(0)
        self.rotor_III.set_position(0)

        # Mensaje de prueba
        mensaje = "HELLO WORLD"
        mensaje_cifrado = self.enigma.encrypt_decrypt(mensaje)
        self.assertNotEqual(mensaje, mensaje_cifrado)

        # Restablecer las posiciones iniciales para descifrar
        self.rotor_I.set_position(0)
        self.rotor_II.set_position(0)
        self.rotor_III.set_position(0)

        mensaje_descifrado = self.enigma.encrypt_decrypt(mensaje_cifrado)
        self.assertEqual(mensaje, mensaje_descifrado)

if __name__ == '__main__':
    unittest.main()
