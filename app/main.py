import sys
import os
import streamlit as st
from enigma.rotor import Rotor
from enigma.reflector import Reflector
from enigma.plugboard import Plugboard
from enigma.enigma_machine import EnigmaMachine

def main():
    st.title("Simulador de Máquina Enigma")

    # Mostrar logo, contacto y sitio web antes de las pestañas
    st.image(
        "https://storage.googleapis.com/allostericsolutionsr/Allosteric_Solutions.png",
        width=400,
    )
    st.write("Contacto:", "franciscocuriel@allostericsolutions.com")
    st.write("Sitio web:", "www.allostericsolutions.com")

    st.write("### Enigma Machine")

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
    plugboard_dict = {}
    for letter in "ABCDEFGHIJKLMNOPQRSTUVWXYZ":
        swap_with = st.selectbox(f"Intercambiar {letter} con", [""] + list("ABCDEFGHIJKLMNOPQRSTUVWXYZ"), key=f"plugboard_{letter}")
        if swap_with and swap_with != letter:
            plugboard_dict[letter] = swap_with
            plugboard_dict[swap_with] = letter

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

    # Mostrar configuración seleccionada
    st.header("Configuración Seleccionada")
    configuracion_seleccionada = f"Rotores: {[rotor_name for rotor_name in selected_rotors]}\n"
    configuracion_seleccionada += f"Posiciones Iniciales: {[rotor.position for rotor in selected_rotors]}\n"
    configuracion_seleccionada += f"Plugboard: {plugboard_dict}"
    st.text_area("Configuración", value=configuracion_seleccionada, height=200)

    # Importar configuración
    st.header("Importar Configuración")
    configuracion_importada = st.text_area("Pega la configuración aquí", height=200)
    if st.button("Aplicar Configuración"):
        # Lógica para aplicar la configuración importada
        aplicar_configuracion(configuracion_importada)

def aplicar_configuracion(configuracion_importada):
    # Parsear y aplicar la configuración importada
    # Ejemplo de formato de configuración importada:
    # Rotores: ['Rotor I', 'Rotor II', 'Rotor III']
    # Posiciones Iniciales: [0, 0, 0]
    # Plugboard: {'A': 'B', 'B': 'A', 'C': 'D', 'D': 'C'}
    try:
        lines = configuracion_importada.split('\n')
        rotors_line = lines[0].split(': ')[1].strip("[]").replace("'", "").split(', ')
        positions_line = [int(x) for x in lines[1].split(': ')[1].strip("[]").split(', ')]
        plugboard_line = eval(lines[2].split(': ')[1])

        # Aplicar la configuración a los selectboxes y sliders
        for i, rotor_name in enumerate(rotors_line):
            st.session_state[f'rotor_{i+1}'] = rotor_name
            st.session_state[f'position_{i}'] = positions_line[i]

        for letter, swap_with in plugboard_line.items():
            st.session_state[f'plugboard_{letter}'] = swap_with

        st.success("Configuración aplicada con éxito")
    except Exception as e:
        st.error(f"Error al aplicar la configuración: {e}")

if __name__ == "__main__":
    main()
