import random

HIDER_SPEED = 1
BUFFER_SIZE = 4096

PLAYER_START_X = 200
PLAYER_START_Y = 200

def gen_uniquie_id(length):
    # Define the characters you want in the random string
    characters = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ" 
    characters += characters.capitalize()
    # Generate a random string of the specified length
    random_string = ''.join(random.choice(characters) for _ in range(length))

    return random_string
