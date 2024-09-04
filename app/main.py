import sys
import os
import streamlit as st
import pyperclip
import json
from enigma.rotor import Rotor
from enigma.reflector import Reflector
from enigma.plugboard import Plugboard
from enigma.enigma_machine import EnigmaMachine

def aplicar_configuracion(configuracion_importada):
    try:
        config = json.loads(configuracion_importada)
        rotors_line = config["Rotores"]
        positions_line = config["Posiciones Iniciales"]
        plugboard_line = config["Plugboard"]

        # Guardar la configuración en el estado de la sesión
        st.session_state['rotors_line'] = rotors_line
        st.session_state['positions_line'] = positions_line
        st.session_state['plugboard_line'] = plugboard_line

        st.success("Configuración aplicada con éxito")
    except Exception as e:
        st.error(f"Error al aplicar la configuración: {e}")

def main():
    st.title("Enigma Machine")

    # Mostrar logo, contacto y sitio web en la barra lateral
    with st.sidebar:
        st.image(
            "https://storage.googleapis.com/allostericsolutionsr/Allosteric_Solutions.png",
            width=360,
        )
        st.write("Contacto:", "franciscocuriel@allostericsolutions.com")
        st.write("Sitio web:", "www.allostericsolutions.com")

    # Importar configuración
    st.header("Importar Configuración")
    configuracion_importada = st.text_area("Pega la configuración aquí", height=200)
    if st.button("Aplicar Configuración"):
        aplicar_configuracion(configuracion_importada)

    # Rotores disponibles
    rotors = {
        "Rotor I": Rotor("EKMFLGDQVZNTOWYHXUSPAIBRCJ", 16),
        "Rotor II": Rotor("AJDKSIRUXBLHWTMCQGZNPYFVOE", 4),
        "Rotor III": Rotor("BDFHJLCPRTXVZNYEIWGAKMUSQO", 21),
        "Rotor IV": Rotor("ESOVPZJAYQUIRHXLNFTGKDCMWB", 9),
        "Rotor V": Rotor("VZBRGITYUPSDNHLXAWMJQOFECK", 25)
    }

    # Reflector disponible
    reflector_B = Reflector("YRUHQSLDPXNGOKMIEBFZCWVJAT")

    # Configuración inicial basada en el estado de la sesión
    if 'rotors_line' in st.session_state:
        rotors_line = st.session_state['rotors_line']
    else:
        rotors_line = ["Rotor I", "Rotor II", "Rotor III"]
    
    if 'positions_line' in st.session_state:
        positions_line = st.session_state['positions_line']
    else:
        positions_line = [0, 0, 0]
    
    if 'plugboard_line' in st.session_state:
        plugboard_line = st.session_state['plugboard_line']
    else:
        plugboard_line = {}

    # Selección de rotores
    st.header("Selección de Rotores")
    selected_rotors = []
    selected_rotor_names = []
    available_rotors = list(rotors.keys())

    for i, rotor_name in enumerate(rotors_line):
        rotor_name = st.selectbox(f"Selecciona el rotor {i+1}", available_rotors, index=available_rotors.index(rotor_name), key=f"rotor_{i+1}")
        selected_rotors.append(rotors[rotor_name])
        selected_rotor_names.append(rotor_name)
        available_rotors.remove(rotor_name)

    # Configuración de la posición inicial de los rotores
    st.header("Posición Inicial de los Rotores")
    rotor_positions = []
    for i, position in enumerate(positions_line):
        position = st.slider(f"Posición inicial del {i+1}° rotor", 0, 25, position, key=f"position_{i}")
        selected_rotors[i].set_position(position)
        rotor_positions.append(position)

    # Configuración del plugboard
    st.header("Configuración del Plugboard")
    plugboard_connections = st.text_input("Introduce las conexiones del plugboard (ej. 'AB CD EF')", " ".join([f"{k}{v}" for k, v in plugboard_line.items()]))
    plugboard_dict = {}
    if plugboard_connections:
        pairs = plugboard_connections.split()
        for pair in pairs:
            if len(pair) == 2:
                plugboard_dict[pair[0].upper()] = pair[1].upper()
                plugboard_dict[pair[1].upper()] = pair[0].upper()
    
    plugboard = Plugboard(plugboard_dict)

    # Crear la máquina Enigma usando la configuración actual
    enigma = EnigmaMachine(selected_rotors, reflector_B, plugboard)

    # Entrada de texto para cifrado/descifrado
    st.header("Cifrado/Descifrado de Mensajes")
    mensaje = st.text_input("Introduce el mensaje:")

    # Botón para cifrar/descifrar
    if st.button("Cifrar/Descifrar"):
        mensaje_cifrado = enigma.encrypt_decrypt(mensaje)
        st.write(f"Mensaje cifrado/descifrado: {mensaje_cifrado}")

    # Mostrar configuración seleccionada
    st.header("Configuración Seleccionada")
    configuracion_seleccionada = json.dumps({
        "Rotores": selected_rotor_names,
        "Posiciones Iniciales": rotor_positions,
        "Plugboard": plugboard_dict
    }, indent=4)
    st.text_area("Configuración", value=configuracion_seleccionada, height=200)

    # Botón de copiado automático usando st.code
    st.code(configuracion_seleccionada, language='json')

if __name__ == "__main__":
    main()
