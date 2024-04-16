import random
import copy

class Room(object):
    turns = ["red_spymaster", "red_operatives", "blue_spymaster", "blue_operatives"]
    def __init__(self, name):
        self.name = name
        self.turn_count = 0
        self.allowed_clicks = 0
        self.current_turn = Room.turns[self.turn_count]
        self.player_count = 0;
        self.red_spymaster = ""
        self.red_operatives = []
        self.red_points = 9
        self.blue_points = 8
        self.blue_spymaster = ""
        self.blue_operatives = []
        self.players = []
        self.spymaster_words = generate_random_words()
        spymaster_words_copy = self.spymaster_words.copy()
        self.words = {x: "" for x in spymaster_words_copy} # Array of {"word": "color"}

    def join_red_spymaster(self, session_id):
        if (len(self.red_spymaster) == 0):
            self.red_spymaster = session_id
            self.player_count += 1

    def join_red_operatives(self, session_id):
        self.red_operatives.append(session_id)
        self.player_count += 1

    def join_blue_spymaster(self, session_id):
        if (len(self.blue_spymaster) == 0):
            self.blue_spymaster =  session_id;
            self.player_count += 1

    def join_blue_operatives(self, session_id):
        self.blue_operatives.append(session_id)
        self.player_count += 1

    def updateTurn(self):
        self.turn_count += 1
        self.current_turn = Room.turns[self.turn_count % len(Room.turns)]
        return self.current_turn
        
    def join_game(self, session_id):
        self.players.append(session_id)
        self.player_count += 1
        
    def update_word_color(self, word):
        if word in self.spymaster_words:
            color = self.spymaster_words[word]
            if color in ["red", "blue", "black", "neutral"]:
                self.words[word] = color
            else:
                print(f"Invalid color '{color}' for word '{word}'")
        else:
            print(f"Invalid word '{word}'")

    def give_clue(self, number):
        self.allowed_clicks = number

    def click_card(self):
        self.allowed_clicks -= 1
        
    def reset_clicks(self):
        self.allowed_clicks = 0
        
    def give_points(self, color):
        if color == "red":
            self.red_points -= 1
        else:
            self.blue_points -= 1
    
    def get_color(self, word):
        correct_color = self.spymaster_words[word]
        self.words[word] = correct_color
        return correct_color
    
    def get_id(self, char):
        if char == 'red_spymaster':
            return self.red_spymaster
        elif char == 'blue_spymaster':
            return self.blue_spymaster
        elif char == 'red_operatives':
            return self.red_operatives
        elif char == 'blue_operatives':
            return self.blue_operatives
    
    def get_points(self):
        return self.red_points, self.blue_points
        
    def __iter__(self):
        return iter((self.red_spymaster, self.blue_spymaster, self.red_operatives, self.blue_operatives, self.red_points, self.blue_points))
    
    def printRoom(self):
        return { "room_name": self.name, "red_spymaster": self.red_spymaster, "blue_spymaster": self.blue_spymaster, "red_operatives": self.red_operatives, "blue_operatives": self.blue_operatives, "red_points": self.red_points, "blue_points": self.blue_points, "words": self.words, "current_turn": self.current_turn, "allowed_clicks": self.allowed_clicks, "player_count": self.player_count }

    
def generate_random_words():
    lines = open('words.txt').read().splitlines()
    red_count = 0
    blue_count = 0
    black_count = 0
    words = {}

    while len(words) != 25:
        word = random.choice(lines)

        # Check if the word is already in the dictionary
        if word not in words:
            if red_count < 9:
                words[word] = "red"
                red_count += 1
            elif blue_count < 8:
                words[word] = "blue"
                blue_count += 1
            elif black_count < 1:
                words[word] = "black"
                black_count += 1
            else:
                words[word] = "neutral"

    # Shuffle the words and their corresponding colors
    shuffled_words = dict(zip(words, random.sample(list(words.values()), len(words))))

    return shuffled_words