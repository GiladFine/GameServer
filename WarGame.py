from Game import *
from Card import *
from Player import *
from Interface import EspInterface
import random

class WarGame(Game):

    def __init__(self, players_list):
        super(WarGame, self).__init__(players_list, Deck([]), [], 0)
        self.deck.generate_full_deck()
        self.esp_interface = Interface.EspInterface('C:\\Users\\idoas\\Documents\\Projects\\E-card\\card_data\\JSON')
        self.has_draw_this_turn_already = {p: False for p in players_list}
        self.has_went_to_war_this_turn_already = {p: False for p in players_list}
        self.current_card_of_player = {p: None for p in players_list}
        self.cards_in_field = []
        self.round_number = 0;
        self.deal_cards()
        self.init_round()

    def button1_handler(player):
        if !self.has_draw_this_turn_already[player]:
            self.has_draw_this_turn_already[player] = True
            self.current_card_of_player[player] = player.hand.pop()
            return {"show_hand": [self.current_card_of_player[player].get_card_name()]}
        else:
            return {"no": []}

    def button2_handler(player):
        if !self.has_went_to_war_this_turn_already[player]:
            self.has_went_to_war_this_turn_already[player] = True
            is_turn_ended = True
            for p in players_list:
                if !self.has_went_to_war_this_turn_already[p]:
                    is_turn_ended = False
                    break
            round_winner = None
            max_card_value = 0
            if is_turn_ended:
                for p in players_list:
                    if self.current_card_of_player[p] == max_card_value:

            return {"show_hand": []}
        else:
            return {"no": []}

    def button3_handler(player):
        return None

    def button4_handler(player):
        return None

    def get_button_names():
        return {1: "Draw (Peak)", 2: "Go To War", 3: "", 4: ""}

    def is_need_to_update_hand(player):
        return {"no": []}

    def deal_cards(self):
        self.deck.shuffle()
        while self.deck.cards_list:
            for player in self.players:
                if self.deck.cards_list:
                    player.add_cards(self.deck.cards_list.pop())

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
