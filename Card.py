import random

VALUES = [1, 2, 3, 4, 5, 6, 7 ,8, 9, 10, 11, 12, 13] #Ace = 1

SHAPES = ["Harts", "Diamonds", "Clubs", "Spades", "Joker"]

SHAPES_SHORTCUTS = ["H", "D", "C", "S", "J"]

VALUES_NAMES = ['A', '2', '3', '4', '5', '6', '7' , '8', '9', '10', 'J', 'Q', 'K']
class Card(object):

    def __init__(self, value, shape):
        self.value = value
        self.shape = shape

    def get_card_name(self):
        if self.shape == 'Joker':
            return self.shape + str(self.value)
        return VALUES_NAMES[VALUES.index(self.value)] + self.shape[0]

    def __eq__(self, other_card):
        if not isinstance(other_card, Card):
            raise NotImplementedError
        return self.value == other_card.value and self.shape == other_card.shape

    def compare(self, other_card):
        if not isinstance(other_card, Card):
            raise NotImplementedError

        if self.shape == 'Joker' and other_card.shape == 'Joker':
            return 0
        if self.shape == 'Joker':
            return 1
        if other_card.shape == 'Joker':
            return -1
        if self.value == other_card.value:
            return 0
        if self.value == 1:
            return 1
        if other_card.value == 1:
            return -1
        return self.value - other_card.value

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
        self.cards_list = [Card(1, "Joker"), Card(2, "Joker")]
        self.cards_list += [Card(value, shape) for value in VALUES for shape in SHAPES[:-1]]
        self.shuffle()
