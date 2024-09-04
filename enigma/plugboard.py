class Plugboard:
    def __init__(self, connections):
        self.connections = connections

    def swap(self, c):
        return self.connections.get(c, c)
