import json

class Player:
    def __init__(self):
        self.deck = self.load_deck()
        self.hand = []

    def load_deck(self):
        with open('data/Cards.json') as f:
            data = json.load(f)
        return data['cards']
