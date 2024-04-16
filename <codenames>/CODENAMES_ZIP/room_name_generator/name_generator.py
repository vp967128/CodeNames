import random

def generate_room_name():
    adjectives = open("./room_name_generator/adjectives.txt").read().splitlines()
    animals = open('./room_name_generator/animals.txt').read().splitlines()
    adjective = random.choice(adjectives)
    animal = random.choice(animals)
    return adjective + '-' + animal
