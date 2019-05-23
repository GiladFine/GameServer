import random

VALUES = [0, 1, 2, 3, 4, 5, 6, 7 ,8, 9, 10, 11, 12, 13] # Joker = 0, Ace = 1

SHAPES = ["Harts", "Diamonds", "Clubs", "Spades", "Joker"]

class Card(object):

    def __init__(self, value, shape):
        self.value = value
        self.shape = shape

    def __eq__(self, other_card):
        if not isinstance(other_card, Card):
            raise NotImplementedError

        return self.value == other_card.value and self.shape == other_card.shape

class Deck(object):

    def __init__(self, cards_list):
        self.cards_list = cards_list # [Card1, Card2 ...]

    def shuffle(self):
        random.shuffle(self.cards_list)

    def hand_out_cards(self, amount):
        return [self.cards_list.pop() for _ in range(amount)]

    def place_cards_on_bottom(self, new_cards):
        for card in new_cards:
            self.cards_list.insert(0, card)

    def place_cards_on_top(self, new_cards):
        for card in new_cards:
            self.cards_list.push(card)

    def generate_full_deck(self):
        self.cards_list = [Card(0, "Joker"), Card(0, "Joker")]
        self.cards_list += [Card(value, shape) for value in VALUES[1:] for shape in SHAPES[:4]]
        self.shuffle()