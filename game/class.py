import json

class field:
    cemetery = []
    void = []
    pose = [[],[],[]]
    def __init__(self):
        pass

class deck:
    card_list = []
    def __init__(self, index):
        data_list = json.load(open('./game/data/Decks.json'))
        card_list = data_list['deck'][index]['cards']
        for card in card_list:
            data_card = json.load(open('./game/data/Cards.json'))
            self.card_list.append(data_card['cards'][card])


dk = deck(1)

print(dk.card_list)
