import socket

import requests
import ctypes
import winsound
import threading


def get_local_ip():
    try:
        host_name = socket.gethostname()
        local_ip = socket.gethostbyname(host_name)
        return local_ip
    except:
        return "127.0.0.1"  # Use localhost if IP detection fails


url = f'http://{get_local_ip()}:5000/secret'
api_key = input("Enter your Secret Key: ")

# Validate username
while True:
    username = input("Enter your username (letters and numbers only, no spaces): ")
    if username.isalnum() and not username.isspace():
        break
    else:
        print("Invalid username. Please enter letters and numbers only without spaces.")

password = input("Enter your password: ")

headers = {
    'X-API-Key': api_key,
    'Content-Type': 'application/json'
}

data = {
    'username': username,
    'password': password
}


def play_sound(sound):
    winsound.PlaySound(sound, winsound.SND_ALIAS)


try:
    response = requests.post(url, headers=headers, json=data)
    response.raise_for_status()  # Raise an HTTPError for bad responses

    # Play a success sound in a separate thread
    threading.Thread(target=play_sound, args=("SystemAsterisk",)).start()

    # Display response in a Windows message box with only OK button
    ctypes.windll.user32.MessageBoxW(0, response.text, "API Response", 0)

except requests.exceptions.RequestException as e:
    # Play an error sound in a separate thread
    threading.Thread(target=play_sound, args=("SystemExclamation",)).start()
    try:
        ctypes.windll.user32.MessageBoxW(0, f"{response.text}", "Request Error", 0)
    except:
        # Display message if there's an issue with the request
        ctypes.windll.user32.MessageBoxW(0, "Application is not Running, run it first", "Request Error", 0)

except Exception as e:
    # Play an error sound in a separate thread
    threading.Thread(target=play_sound, args=("SystemExclamation",)).start()

    # Handle other exceptions and display a generic error message
    ctypes.windll.user32.MessageBoxW(0, f"An unexpected error occurred: {e}", "Error", 0)
