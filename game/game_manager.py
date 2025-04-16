from .deck import PlayerDeck
from network.client import GameClient

class GameManager:
    def __init__(self):
        self.player1_deck = PlayerDeck()
        self.player2_deck = PlayerDeck()
        self.current_player = 2  # 1 or 2
        self.game_started = False

    def start_game(self):
        """Initialize the game and deal initial hands"""
        self.game_started = True
        # Deal initial hands (e.g., 5 cards each)
        for _ in range(5):
            self.player1_deck.draw_to_hand()
            self.player2_deck.draw_to_hand()

    def draw_card(self, player_number):
        """Draw a card for the specified player"""
        if not self.game_started:
            return None
        
        if player_number == 1:
            return self.player1_deck.draw_to_hand()
        elif player_number == 2:
            return self.player2_deck.draw_to_hand()
        return None

    def get_player_hand(self, player_number):
        """Get the hand of the specified player"""
        if player_number == 1:
            return self.player1_deck.get_hand()
        elif player_number == 2:
            return self.player2_deck.get_hand()
        return []

    def switch_player(self):
        """Switch the current player"""
        self.current_player = 3 - self.current_player  # Switches between 1 and 2

    def is_player_turn(self, player_number):
        """Check if it's the specified player's turn"""
        return self.current_player == player_number

    def get_current_player(self):
        """Get the current player number"""
        return self.current_player 