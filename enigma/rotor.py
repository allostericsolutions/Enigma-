class Rotor:
    def __init__(self, wiring, notch):
        self.wiring = wiring
        self.notch = notch
        self.position = 0

    def set_position(self, position):
        self.position = position

    def forward(self, c):
        index = (ord(c) - ord('A') + self.position) % 26
        encrypted_char = self.wiring[index]
        return chr((ord(encrypted_char) - ord('A') - self.position) % 26 + ord('A'))

    def backward(self, c):
        index = (ord(c) - ord('A') + self.position) % 26
        decrypted_index = (self.wiring.index(chr(index + ord('A'))) - self.position) % 26
        return chr(decrypted_index + ord('A'))

    def rotate(self):
        self.position = (self.position + 1) % 26
        return self.position == self.notch
