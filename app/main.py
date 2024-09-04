import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import streamlit as st
from enigma.rotor import Rotor
from enigma.reflector import Reflector
from enigma.plugboard import Plugboard
from enigma.enigma_machine import EnigmaMachine

# Definición de los rotores disponibles
rotors = {
    "Rotor I": Rotor("EKMFLGDQVZNTOWYHXUSPAIBRCJ", 16),
    "Rotor II": Rotor("AJDKSIRUXBLHWTMCQGZNPYFVOE", 4),
    "Rotor III": Rotor("BDFHJLCPRTXVZNYEIWGAKMUSQO", 21),
    "Rotor IV": Rotor("ESOVPZJAYQUIRHXLNFTGKDCMWB", 9),
    "Rotor V": Rotor("VZBRGITYUPSDNHLXAWMJQOFECK", 25)
}

# Definición del reflector
reflector_B = Reflector("YRUHQSLDPXNGOKMIEBFZCWVJAT")

# Título de la aplicación
st.title("Simulador de Máquina Enigma")

# Selección de rotores
st.header("Selección de Rotores")
selected_rotors = []
for i in range(1, 4):
    rotor_name = st.selectbox(f"Selecciona el rotor {i}", list(rotors.keys()), key=f"rotor_{i}")
    selected_rotors.append(rotors[rotor_name])

# Configuración de la posición inicial de los rotores
st.header("Posición Inicial de los Rotores")
for i, rotor in enumerate(selected_rotors):
    position = st.slider(f"Posición inicial del {i+1}° rotor", 0, 25, 0, key=f"position_{i}")
    rotor.set_position(position)

# Configuración del plugboard
st.header("Configuración del Plugboard")
plugboard_connections = st.text_input("Introduce las conexiones del plugboard (ej. 'AB CD EF')", "")
plugboard_dict = {}
if plugboard_connections:
    pairs = plugboard_connections.split()
    for pair in pairs:
        if len(pair) == 2:
            plugboard_dict[pair[0].upper()] = pair[1].upper()
            plugboard_dict[pair[1].upper()] = pair[0].upper()

plugboard = Plugboard(plugboard_dict)

# Crear la máquina Enigma
enigma = EnigmaMachine(selected_rotors, reflector_B, plugboard)

# Entrada de texto
st.header("Cifrado/Descifrado de Mensajes")
mensaje = st.text_input("Introduce el mensaje:")

# Botón para cifrar/descifrar
if st.button("Cifrar/Descifrar"):
    mensaje_cifrado = enigma.encrypt_decrypt(mensaje)
    st.write(f"Mensaje cifrado/descifrado: {mensaje_cifrado}")
