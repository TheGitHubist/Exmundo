import json

class field:
    cemetery = []
    void = []
    pose = [[],[],[]]
    def __init__(self):
        pass

class deck:
    def __init__(self, index):
        data = json.load(open('./game/data/Deck.json'))
        self.card_list = data['deck'][index]

dk = deck(1)

print(dk.card_list)
