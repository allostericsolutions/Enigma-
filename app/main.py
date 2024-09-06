
import sys
import os
import streamlit as st
import pyperclip
import json
from enigma.rotor import Rotor
from enigma.reflector import Reflector
from enigma.plugboard import Plugboard
from enigma.enigma_machine import EnigmaMachine

def apply_configuration(imported_config):
    try:
        config = json.loads(imported_config)
        rotors_line = config["Rotors"]
        positions_line = config["Initial Positions"]
        plugboard_line = config["Plugboard"]

        # Store the configuration in session state
        st.session_state['rotors_line'] = rotors_line
        st.session_state['positions_line'] = positions_line
        st.session_state['plugboard_line'] = plugboard_line

        st.success("Configuration applied successfully")
    except Exception as e:
        st.error(f"Error applying configuration: {e}")

def main():
    st.title("Enigma Machine")

    # Show logo, contact and website in the sidebar
    with st.sidebar:
        st.image(
            "https://storage.googleapis.com/allostericsolutionsr/Allosteric_Solutions.png",
            width=360,
        )
        st.write("Contact:", "franciscocuriel@allostericsolutions.com")
        st.write("Website:", "www.allostericsolutions.com")

    # Import configuration
    st.header("Import Configuration")
    imported_config = st.text_area("Paste the configuration here", height=200)
    if st.button("Apply Configuration"):
        apply_configuration(imported_config)

    # Available rotors
    rotors = {
        "Rotor I": Rotor("EKMFLGDQVZNTOWYHXUSPAIBRCJ", 16),
        "Rotor II": Rotor("AJDKSIRUXBLHWTMCQGZNPYFVOE", 4),
        "Rotor III": Rotor("BDFHJLCPRTXVZNYEIWGAKMUSQO", 21),
        "Rotor IV": Rotor("ESOVPZJAYQUIRHXLNFTGKDCMWB", 9),
        "Rotor V": Rotor("VZBRGITYUPSDNHLXAWMJQOFECK", 25)
    }

    # Available reflector
    reflector_B = Reflector("YRUHQSLDPXNGOKMIEBFZCWVJAT")

    # Initial configuration based on session state
    if 'rotors_line' in st.session_state:
        rotors_line = st.session_state['rotors_line']
    else:
        rotors_line = ["Rotor I", "Rotor II", "Rotor III"]
    
    if 'positions_line' in st.session_state:
        positions_line = st.session_state['positions_line']
    else:
        positions_line = ["A", "A", "A"]
    
    if 'plugboard_line' in st.session_state:
        plugboard_line = st.session_state['plugboard_line']
    else:
        plugboard_line = {}

    # Rotor selection
    st.header("Rotor Selection")
    selected_rotors = []
    selected_rotor_names = []
    available_rotors = list(rotors.keys())

    for i, rotor_name in enumerate(rotors_line):
        if rotor_name not in available_rotors:
            rotor_name = available_rotors[0]  # Default to the first available rotor if not found
        rotor_name = st.selectbox(f"Select rotor {i+1}", available_rotors, index=available_rotors.index(rotor_name), key=f"rotor_{i+1}")
        selected_rotors.append(rotors[rotor_name])
        selected_rotor_names.append(rotor_name)
        available_rotors.remove(rotor_name)

    # Initial rotor positions
    st.header("Initial Rotor Positions")
    rotor_positions = []
    alphabet = [chr(i) for i in range(ord('A'), ord('Z') + 1)]
    for i, position in enumerate(positions_line):
        if position not in alphabet:
            position = "A"  # Default to 'A' if the position is not valid
        position = st.selectbox(f"Initial position of rotor {i+1}", alphabet, index=alphabet.index(position), key=f"position_{i}")
        selected_rotors[i].set_position(alphabet.index(position))
        rotor_positions.append(position)

    # Plugboard configuration
    st.header("Plugboard Configuration")
    plugboard_connections = st.text_input("Enter the plugboard connections (e.g. 'AB CD EF')", " ".join([f"{k}{v}" for k, v in plugboard_line.items()]))
    plugboard_dict = {}
    if plugboard_connections:
        pairs = plugboard_connections.split()
        for pair in pairs:
            if len(pair) == 2:
                plugboard_dict[pair[0].upper()] = pair[1].upper()
                plugboard_dict[pair[1].upper()] = pair[0].upper()
    
    plugboard = Plugboard(plugboard_dict)

    # Create the Enigma machine with the current configuration
    enigma = EnigmaMachine(selected_rotors, reflector_B, plugboard)

    # Text input for encryption/decryption
    st.header("Message Encryption/Decryption")
    message = st.text_input("Enter the message:")

    # Button for encryption/decryption
    if st.button("Encrypt/Decrypt"):
        encrypted_message = enigma.encrypt_decrypt(message)
        st.write(f"Encrypted/Decrypted message: {encrypted_message}")

    # Show selected configuration
    st.header("Selected Configuration")
    selected_config = json.dumps({
        "Rotors": selected_rotor_names,
        "Initial Positions": rotor_positions,
        "Plugboard": plugboard_dict
    }, indent=4)
    st.text_area("Configuration", value=selected_config, height=200)

    # Auto copy button using st.code
    st.code(selected_config, language='json')

if __name__ == "__main__":
    main()
