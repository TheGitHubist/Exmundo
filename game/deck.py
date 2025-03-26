import random
from .cards import CardModel

class Deck:
    def __init__(self, cards=None):
        self.cards = cards if cards is not None else []
        self.shuffle()

    def shuffle(self):
        """Shuffle the deck"""
        random.shuffle(self.cards)

    def draw_card(self):
        """Draw a card from the top of the deck"""
        if len(self.cards) > 0:
            return self.cards.pop()
        return None

    def add_card(self, card):
        """Add a card to the deck"""
        self.cards.append(card)

    def add_cards(self, cards):
        """Add multiple cards to the deck"""
        self.cards.extend(cards)

    def is_empty(self):
        """Check if the deck is empty"""
        return len(self.cards) == 0

    def get_card_count(self):
        """Get the number of cards in the deck"""
        return len(self.cards)

class PlayerDeck(Deck):
    def __init__(self, cards=None):
        super().__init__(cards)
        self.hand = []
        self.max_hand_size = 7  # Maximum number of cards a player can have in hand

    def draw_to_hand(self):
        """Draw a card and add it to the player's hand"""
        if len(self.hand) < self.max_hand_size:
            card = self.draw_card()
            if card:
                self.hand.append(card)
                return card
        return None

    def get_hand(self):
        """Get the current hand"""
        return self.hand

    def remove_from_hand(self, card):
        """Remove a card from the hand"""
        if card in self.hand:
            self.hand.remove(card)
            return True
        return False 