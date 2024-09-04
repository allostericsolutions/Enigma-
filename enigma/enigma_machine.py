from .rotor import Rotor
from .reflector import Reflector
from .plugboard import Plugboard

class EnigmaMachine:
    def __init__(self, rotors, reflector, plugboard):
        self.rotors = rotors
        self.reflector = reflector
        self.plugboard = plugboard

    def encrypt_decrypt(self, text):
        result = []
        for char in text:
            if char.isalpha():
                char = char.upper()
                char = self.plugboard.swap(char)
                for rotor in self.rotors:
                    char = rotor.forward(char)
                char = self.reflector.reflect(char)
                for rotor in reversed(self.rotors):
                    char = rotor.backward(char)
                char = self.plugboard.swap(char)
                result.append(char)
                for rotor in self.rotors:
                    if not rotor.rotate():
                        break
            else:
                result.append(char)
        return ''.join(result)
