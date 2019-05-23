from Game import *
from Card import *
from Player import *

SLICERS = [Card(0, "Joker"), Card(2, "Harts"), Card(2, "Diamonds"), Card(2, "Spades"), Card(2, "Clubs")]

class PresidentGame(Game):

    def __init__(self, players_list):
        super(PresidentGame, self).__init__(players_list, Deck([]), [], 0)
        self.current_ranking = []
        self.best_rank_available = 0
        self.worst_rank_available = len(players_list) - 1
        self.deck.generate_full_deck()
        self.deal_cards()
        self.init_round(self.get_player_with_card(Card(3, "Clubs")))


    def deal_cards(self):
        k, m = divmod(len(self.deck.cards_list), len(self.players))
        divided_list = list(self.deck.cards_list[i * k + min(i, m):(i + 1) * k + min(i + 1, m)] for i in range(len(self.players)))
        for player in self.players:
            player.hand = divided_list[self.players.index(player)]

        self.deck = Deck([])

    def init_round(self, player_index):
        self.current_ranking = []
        self.best_rank_available = 0
        self.worst_rank_available = len(self.players) - 1

        for player in self.players:
            player.set_is_active(True)

        self.deck.generate_full_deck()
        self.deal_cards()
        self.set_current_player(player_index)


    def conclude_results(self):
        for i in self.current_ranking:
            print(str(i + 1) + ". " + self.players[i])

    def is_card_slicer(self, card):
        return card in SLICERS

    def has_game_ended(self):
        for player in self.players:
            if len(player.hand) == 0:
                self.current_ranking[self.best_rank_available] = self.active_player_index
                print (player.name + " is the Winner!")
                return True

            if all(card.value == 2 for card in player.hand):
                self.current_ranking[self.worst_rank_available] = self.active_player_index
                print(player.name + " is the Loser!")
                return True

        return False

    def do_turn(self):
        cards_to_be_played = [] #ToDo - UI
        self.play_cards(cards_to_be_played)
        if len(cards_to_be_played) == 1 and self.is_card_slicer(cards_to_be_played[0]):
            self.burn_middle()
            cards_to_be_played = []  # ToDo - UI
            self.play_cards(cards_to_be_played)

    def end_rule(self):
        return not any(player.isActive for player in self.players)

    def run_game(self):
        while True:
            while not self.end_rule():
                self.do_turn()
                if self.has_game_ended():
                    self.active_player.set_is_active(False)
                else:
                    self.next_player()

            self.conclude_results()
            self.init_round(self.current_ranking[-1])
            self.next_player()
