from .deck import PlayerDeck

class GameManager:
    def __init__(self):
        self.player_deck = PlayerDeck()
        self.current_player = 1

    def get_player_hand(self, player_number):
        """Get the hand of the specified player"""
        pass