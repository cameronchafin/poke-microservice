import socket
import requests

# Define the address and port for the microservice
HOST = "127.0.0.1"  # Update with your microservice's IP address or hostname
PORT = 12345  # Update with the microservice's port


# Function to fetch evolution data from the Pokémon API
def fetch_pokemon_evolutions(pokemon_name):
    try:
        # Make a request to the Pokémon API to fetch species data
        species_response = requests.get(f"https://pokeapi.co/api/v2/pokemon-species/{pokemon_name}/")
        species_data = species_response.json()

        # Extract the evolution chain URL from the species data
        evolution_chain_url = species_data.get("evolution_chain", {}).get("url")

        # Make a request to the evolution chain URL to fetch evolution data
        evolution_chain_response = requests.get(evolution_chain_url)
        evolution_chain_data = evolution_chain_response.json()

        # Extract evolution information
        evolutions = []
        current_pokemon = evolution_chain_data.get("chain")
        while current_pokemon:
            pokemon_name = current_pokemon["species"]["name"]
            evolutions.append(pokemon_name)
            current_pokemon = current_pokemon.get("evolves_to")[0] if current_pokemon.get("evolves_to") else None

        return evolutions

    except Exception as e:
        # Handle any exceptions that may occur during the API request
        print(f"Error fetching evolution data: {str(e)}")

    return None


# Set up the microservice's socket server
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((HOST, PORT))
server_socket.listen(5)

while True:
    client_socket, addr = server_socket.accept()
    data = client_socket.recv(1024).decode("utf-8")

    if data.startswith("GET_EVOLUTIONS "):
        # Extract the Pokémon name from the command
        pokemon_name = data.split(" ")[1]

        # Fetch evolution data for the specified Pokémon
        evolutions = fetch_pokemon_evolutions(pokemon_name)

        if evolutions is not None:
            # Send the evolution data as a response to the Tkinter application
            response_data = "\n".join(evolutions)
            client_socket.send(response_data.encode("utf-8"))
        else:
            # Handle errors when fetching evolution data
            error_message = "Error fetching evolution data for the specified Pokémon."
            client_socket.send(error_message.encode("utf-8"))

    client_socket.close()
