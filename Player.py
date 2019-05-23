
class Player(object):

    def __init__(self, name, cards_list):
        self.name = name
        self.hand = cards_list
        self.current_card_index = 0
        self.score = 0
        self.isActive = True

    def __eq__(self, other_player):
        if not isinstance(other_player, Player):
            raise NotImplementedError

        return self.name == other_player.name and self.hand == other_player.hand


    def move_right(self):
        self.current_card_index = (self.current_card_index + 1) % len(self.hand)

    def move_left(self):
        self.current_card_index = (self.current_card_index - 1) % len(self.hand)

    def add_cards(self, cards_list):
        self.hand.append(cards_list)

    def remove_cards(self, cards_list):
        self.hand = [card for card in self.hand if card not in cards_list]
        self.current_card_index = 0

    def set_is_active(self, isActive):
        self.isActive = isActive

    def validate_cards(self, cards_list):
        """
        Checks if cards_list exist in player's hand
        :param cards_list:
        :return:
        """
        return set(self.hand).issubset(set(cards_list))