import game_flask_server


class Game(object):

    def __init__(self, players_list, deck, middle, first_player):
        game_flask_server.app_ip_to_player.update({p.app_ip:p for p in players_list})
        game_flask_server.game = self
        self.players = players_list
        self.deck = deck
        self.middle = middle # Where everybody tosses their cards
        self.active_player_index = first_player # Index of the player that's playing now
        self.active_player = self.players[self.active_player_index]
        self.turn_counter = 0
        self.start = game_flask_server.run_server

    def end_rule(self):
        raise NotImplementedError

    def button1_handler():
        raise NotImplementedError

    def button2_handler():
        raise NotImplementedError

    def button3_handler():
        raise NotImplementedError

    def button4_handler():
        raise NotImplementedError

    def get_button_names():
        raise NotImplementedError

    def is_need_to_update_hand():
        raise NotImplementedError

    def run_game(self):
        """
        Main game logic
        :return:
        """
        raise NotImplementedError

    def do_turn(self):
        """
        One turn logic
        :return:
        """
        raise NotImplementedError

    def get_player_input(self):
        # ToDo - implement UI and receive command
        raise NotImplementedError

    def set_current_player(self, player_index):
        self.active_player_index = player_index % len(self.players)
        self.active_player = self.players[self.active_player_index]

    def deal_cards(self):
        """
        Initial dealing of the game
        :return:
        """
        raise NotImplementedError # Empty deck logic depend on sub-class

    def next_player(self):
        self.set_current_player(self.active_player_index + 1)

    def pre_draw(self, cards, action):
        raise NotImplementedError # Implementation per sub-class

    def draw(self, amount):
        """
        Draw from deck
        :param amount:
        :return:
        """
        self.active_player.add_cards(self.deck.hand_out_cards(amount))

    def post_draw(self, cards, action):
        raise NotImplementedError  # Implementation per sub-class

    def replace_cards(self, player_1_index, player_1_cards, player_2_index, player_2_cards):
        """
        Replace cards between 2 players
        :param player_1_index:
        :param player_1_cards:
        :param player_2_index:
        :param player_2_cards:
        :return:
        """
        if player_1_index == player_2_index:
            raise ValueError("Error, player can't replace cards with himself!!")

        player1 = self.players[player_1_index]
        player2 = self.players[player_2_index]
        player1.remove_cards(player_1_cards)
        player1.active_player.add_cards(player_2_cards)
        player2.remove_cards(player_2_cards)
        player2.add_cards(player_1_cards)

    def play_cards(self, cards):
        """
        Plays the cards by placing them in the middle
        :param cards:
        :return:
        """
        if not self.active_player.validate_cards(cards):
            raise ("Error, can't play cards you don't have....")

        self.active_player.remove_cards(cards)
        self.middle.append(cards)

    def burn_cards(self, cards):
        """
        Remove cards from game
        :param cards:
        :return:
        """
        self.active_player.remove_cards(cards)

    def burn_middle(self):
        """
        Remove middle cards from game
        :return:
        """
        self.middle = []

    def place_middle_in_deck(self):
        """
        Place middle in bottom of the deck
        :return:
        """
        self.deck.cards_list.place_cards_on_bottom(self.middle)
        self.middle = []

    def shuffle_deck(self):
        self.deck.cards_list.shuffle()

    def get_player_with_card(self, card):
        """
        Returns index of player containing the card
        :param card:
        :return:
        """
        if card in self.deck.cards_list:
            raise ValueError("Error, The card is in the deck")

        for player in self.players:
            if card in player.hand:
                return self.players.index(player)

        raise ValueError("Error, Card was not found")
