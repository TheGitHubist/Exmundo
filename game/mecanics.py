class Turn:
    def __init__(self, player):
        self.player = player
    
    def drawPhase(self):
        if self.player.deck:
            card = self.player.deck.pop(0)
            self.player.hand.append(card)
            return card
        return None

    def battleMonsters(self):
        pass

    def endPhase(self):
        pass