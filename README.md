# Pokémon Evolution Microservice README

## Communication Contract

### Introduction

This README outlines the communication contract for interacting with the microservice implemented in this project. 
The microservice acts as an intermediary between client applications and the Pokémon API, allowing clients to request and receive Pokémon data programmatically.

### Requesting Data

#### Command: `GET_EVOLUTIONS`

- To request evolution data for a specific Pokémon, send a command in the following format:


- Replace `[Pokemon Name]` with the name of the Pokémon for which you want to fetch evolution data.

#### Example Request Call (Python):

```python
import socket

HOST = "127.0.0.1"  # Replace with the microservice's IP address or hostname
PORT = 12345        # Replace with the microservice's port

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((HOST, PORT))

# Send a "GET_EVOLUTIONS" command with a Pokémon name
pokemon_name = "pikachu"  # Replace with the desired Pokémon name
command = f"GET_EVOLUTIONS {pokemon_name}"
client_socket.send(command.encode("utf-8"))

# Receive and print the response from the microservice
response = client_socket.recv(1024).decode("utf-8")
print(response)

client_socket.close()
```

### Receiving Data

- The microservice will respond to the request with a newline-separated list of Pokémon names representing the evolution chain. The data will be received as a string.

#### Example Response:

Pichu<br>
Pikachu<br>
Raichu

### UML Sequence Diagram

**Figure 1:** UML Sequence Diagram for Pokémon Evolution Microservice Interaction

![Blank diagram](https://github.com/cameronchafin/poke-microservice/assets/63039479/6d765311-bb87-4d4e-969e-37576183c62d)

