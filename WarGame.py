from Game import *
from Card import *
from Player import *
from Interface import EspInterface
import random
import game_flask_server
import threading

class WarGame(Game):

    def __init__(self, players_list):
        super(WarGame, self).__init__(players_list, Deck([]), [], 0)
        self.deck.generate_full_deck()
        self.esp_interface = EspInterface('C:\\Users\\idoas\\Documents\\Projects\\E-card\\card_data\\JSONS\\')
        self.has_draw_this_turn_already = {p: False for p in players_list}
        self.has_went_to_war_this_turn_already = {p: False for p in players_list}
        self.current_card_of_player = {p: None for p in players_list}
        self.index_of_card_during_war = {p: None for p in players_list}
        self.stash = {p: [] for p in players_list}
        self.earns_card = []
        self.round_winner = None
        self.told_round_winner = {p: False for p in players_list}
        self.has_opened_card = False
        self.round_number = 0
        self.deal_cards()
        self.start()
        # self.init_round()

    def button1_handler(self, player):
        if not self.has_draw_this_turn_already[player]:


            self.has_draw_this_turn_already[player] = True
            player_card = player.hand.pop()
            self.current_card_of_player[player] = player_card
            if self.has_opened_card:
                while self.current_card_of_player[self.players_list[0]].value == self.current_card_of_player[self.players_list[1]].value:
                    player.hand.insert(0, player_card)
                    player_card = player.hand.pop()
                    self.current_card_of_player[player] = player_card
                self.has_opened_card = False
            else:
                self.has_opened_card = True
            self.earns_card.append(player_card)
            self.stash[player].append(player_card)
            print "\n\n\n*************", player.name, [(c,type(c)) for c in self.stash[player]], "**************\n\n\n"
            if self.index_of_card_during_war[player]:
                self.index_of_card_during_war[player] += 1
            print {"command": "show_hand", "args": [stash_card.get_card_name() for stash_card in self.stash[player]]}
            return {"command": "show_hand", "args": [stash_card.get_card_name() for stash_card in self.stash[player]]}
        else:
            print "nop"
            return {"command":"no", "args": []}

    def button2_handler(self, player):
        if self.index_of_card_during_war[player] and self.index_of_card_during_war[player] < 2:
            print {"command": "show_hand and message",
                    "args": [card.get_card_name() for card in self.stash[player]],
                    "string": "Draw {} more cards".format(3 - self.index_of_card_during_war[Player])
                    }
            return {"command": "show_hand and message",
                    "args": [card.get_card_name() for card in self.stash[player]],
                    "string": "Draw {} more cards".format(3 - self.index_of_card_during_war[Player])
                    }
        if self.has_went_to_war_this_turn_already[player]:
            print "nop"
            return {"command":"no", "args": []}
        self.has_went_to_war_this_turn_already[player] = True
        for p in self.players_list:
            if not self.has_went_to_war_this_turn_already[p]:
                is_turn_ended = False
                break
        is_turn_ended = True
        current_round_winner = None
        if is_turn_ended:
            result = self.current_card_of_player[self.players_list[0]].compare(self.current_card_of_player[self.players_list[1]])
            if result == 0:
                self.index_of_card_during_war = {p: 0 for p in self.players_list}
                print {"command":"message", "string": "There is a tie. Draw 3 cards"}
                return {"command":"message", "string": "There is a tie. Draw 3 cards"}
            else:
                current_round_winner = self.players_list[0]
                if result < 0:
                    current_round_winner = self.players_list[1]
                current_round_winner.hand = self.earns_card + current_round_winner.hand
                self.round_winner = current_round_winner
                self.has_draw_this_turn_already = {p: False for p in self.players_list}
                self.earns_card = []
                self.stash = {p: [] for p in self.players_list}
                self.index_of_card_during_war = {p: None for p in self.players_list}
                self.has_went_to_war_this_turn_already = {p: False for p in self.players_list}
                self.can_tell_score = {p: True for p in self.players_list}
        #self.esp_interface.send_card(player.esp_ip, self.current_card_of_player[player])
        is_turn_ended = True
        thread = threading.Thread(target=self.esp_interface.send_card, args=(player.esp_ip, self.current_card_of_player[player]))
        thread.start()
        print {"command": "show_hand", "args": []}
        return {"command": "show_hand", "args": []}


    def ask_state(self, player):
        if not self.can_tell_score[player]:
            print "nop"
            return {"command":"no", "args": []}
        self.can_tell_score[player] = False
        if self.index_of_card_during_war[player]:
            print {"command":"message", "string": "There is a tie. Draw 3 cards"}
            return {"command":"message", "string": "There is a tie. Draw 3 cards"}
        else:
            print {"command":"message", "string": "You {} this round.\n You have {} cards.".format(
                            "won" if player.app_ip == self.round_winner.app_ip else "lost",
                            len(player.hand))}
            return {"command":"message", "string": "You {} this round.\n You have {} cards.".format(
                    "won" if player.app_ip == self.round_winner.app_ip else "lost",
                    len(player.hand))}

    def button3_handler(self, player):
        print "nop"
        return {"command":"no", "args": []}

    def button4_handler(self, player):
        print "nop"
        return {"command":"no", "args": []}

    def get_button_names(self):
        return {"1": "Draw (Peak)", "2": "Go To War", "3": "", "4": ""}

    def is_need_to_update_hand(self, player):
        return {"command":"no", "args": []}

    def deal_cards(self):
        self.deck.shuffle()
        while self.deck.cards_list:
            for player in self.players_list:
                if self.deck.cards_list:
                    player.add_cards(self.deck.cards_list.pop())

    def init_round(self, player_index):
        self.current_ranking = []
        self.best_rank_available = 0
        self.worst_rank_available = len(self.players_list) - 1

        for player in self.players_list:
            player.set_is_active(True)

        self.deck.generate_full_deck()
        self.deal_cards()
        self.set_current_player(player_index)


    def conclude_results(self):
        for i in self.current_ranking:
            print(str(i + 1) + ". " + self.players_list[i])

    def is_card_slicer(self, card):
        return card in SLICERS

    def has_game_ended(self):
        for player in self.players_list:
            if len(player.hand) == 0:
                print (player.name + " is the Losser!")
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
        return not any(player.isActive for player in self.players_list)

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
