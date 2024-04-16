def generate_room_name():
    adjectives = open("adjectives.txt", 'r').splitlines()
    animals = open('animals.txt', 'r').splitlines()
    adjective = random.choice(adjectives)
    animal = random.choice(animals)
    return adjective + '-' + animal
    
print(generate_room_name())