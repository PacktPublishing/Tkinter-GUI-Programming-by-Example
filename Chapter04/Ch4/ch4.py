import tkinter as tk

from functools import partial

from casino import Card, Deck, Player, Dealer, assets_folder
from casino_sounds import SoundBoard


class GameScreen(tk.Canvas):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

        self.DECK_COORDINATES = (700, 100)

        self.CARD_ORIGINAL_POSITION = 100
        self.CARD_WIDTH_OFFSET = 100

        self.PLAYER_CARD_HEIGHT = 300
        self.DEALER_CARD_HEIGHT = 100

        self.PLAYER_SCORE_TEXT_COORDS = (340, 450)
        self.PLAYER_MONEY_COORDS = (490, 450)
        self.POT_MONEY_COORDS = (500, 100)
        self.WINNER_TEXT_COORDS = (400, 250)

        self.game_state = GameState()
        self.sound_board = SoundBoard()

        self.tabletop_image = tk.PhotoImage(file=assets_folder + "/tabletop.png")
        self.card_back_image = Card.get_back_file()

        self.player_score_text = None
        self.player_money_text = None
        self.pot_money_text = None
        self.winner_text = None

        self.cards_to_deal_pointer = 0
        self.frame = 0

    def refresh(self):
        self.game_state = GameState()

    def setup_opening_animation(self):
        self.sound_board.shuffle_sound.play()
        self.create_image((400, 250), image=self.tabletop_image)

        self.card_back_1 = self.create_image(self.DECK_COORDINATES, image=self.card_back_image)
        self.card_back_2 = self.create_image((self.DECK_COORDINATES[0] + 20, self.DECK_COORDINATES[1]), image=self.card_back_image)

        self.back_1_movement = ([10] * 6 + [-10] * 6) * 7
        self.back_2_movement = ([-10] * 6 + [10] * 6) * 7

        self.play_card_animation()

    def play_card_animation(self):
        if self.frame < len(self.back_1_movement):
            self.move(self.card_back_1, self.back_1_movement[self.frame], 0)
            self.move(self.card_back_2, self.back_2_movement[self.frame], 0)
            self.update()
            self.frame += 1

            self.after(33, self.play_card_animation)
        else:
            self.delete(self.card_back_2)
            self.frame = 0
            self.display_table()

    def play_deal_animation(self):
        self.playing_animation = True
        self.animation_frames = 15

        self.card_back_2 = self.create_image(self.DECK_COORDINATES, image=self.card_back_image)

        target_coords = self.cards_to_deal_positions[self.cards_to_deal_pointer]

        x_diff = self.DECK_COORDINATES[0] - target_coords[0]
        y_diff = self.DECK_COORDINATES[1] - target_coords[1]

        x_step = (x_diff / self.animation_frames) * -1
        y_step = (y_diff / self.animation_frames) * -1

        self.move_func = partial(self.move_card, item=self.card_back_2, x_dist=x_step, y_dist=y_step)
        self.move_func.__name__ = 'move_card'

        self.move_card(self.card_back_2, x_step, y_step)

    def move_card(self, item, x_dist, y_dist):
        self.move(item, x_dist, y_dist)
        self.update()
        self.frame += 1
        if self.frame < self.animation_frames:
            self.after(33, self.move_func)
        else:
            self.frame = 0
            self.delete(self.card_back_2)
            self.show_card()
            self.sound_board.place_sound.play()

            if self.cards_to_deal_pointer < (len(self.cards_to_deal_images) - 1):
                self.cards_to_deal_pointer += 1
                self.play_deal_animation()
            else:
                self.cards_to_deal_pointer = 0
                self.cards_to_deal_images = []
                self.cards_to_deal_positions = []
                self.playing_animation = False

    def show_card(self):
        self.create_image(
            self.cards_to_deal_positions[self.cards_to_deal_pointer],
            image=self.cards_to_deal_images[self.cards_to_deal_pointer]
        )
        self.update()

    def hit(self):
        self.master.remove_all_buttons()
        new_card = self.game_state.draw()
        card_number = len(self.game_state.player.hand.cards)
        image_pos = self.get_player_card_pos(card_number)

        self.cards_to_deal_images.append(new_card.get_file())
        self.cards_to_deal_positions.append(image_pos)

        self.play_deal_animation()

        while self.playing_animation:
            self.master.update()

        self.game_state.hit(new_card)
        self.update_text()
        self.check_for_winner()

    def stick(self):
        table_state = self.game_state.calculate_final_state()

        self.show_dealers_cards(table_state)
        self.show_winner_text(table_state['has_winner'])
        self.master.on_winner()

    def show_dealers_cards(self, table_state):
        dealer_first_card = table_state['dealer_cards'][0].get_file()
        self.create_image((self.CARD_ORIGINAL_POSITION, self.DEALER_CARD_HEIGHT), image=dealer_first_card)

    def check_for_winner(self):
        winner = self.game_state.check_for_winner()

        if winner:
            self.show_dealers_cards(self.game_state.get_table_state())
            self.show_winner_text(winner)
            self.master.on_winner()
        else:
            self.master.show_gameplay_buttons()

    def get_player_card_pos(self, card_number):
        return (self.CARD_ORIGINAL_POSITION + self.CARD_WIDTH_OFFSET * card_number, self.PLAYER_CARD_HEIGHT)

    def display_table(self, hide_dealer=True, table_state=None):
        if not table_state:
            table_state = self.game_state.get_table_state()

        player_card_images = [card.get_file() for card in table_state['player_cards']]
        dealer_card_images = [card.get_file() for card in table_state['dealer_cards']]
        if hide_dealer and not table_state['blackjack']:
            dealer_card_images[0] = Card.get_back_file()

        self.cards_to_deal_images = []
        self.cards_to_deal_positions = []

        for card_number, card_image in enumerate(player_card_images):
            image_pos = self.get_player_card_pos(card_number)
            self.cards_to_deal_images.append(card_image)
            self.cards_to_deal_positions.append(image_pos)

        for card_number, card_image in enumerate(dealer_card_images):
            image_pos = (self.CARD_ORIGINAL_POSITION + self.CARD_WIDTH_OFFSET * card_number, self.DEALER_CARD_HEIGHT)
            self.cards_to_deal_images.append(card_image)
            self.cards_to_deal_positions.append(image_pos)

        self.play_deal_animation()

        while self.playing_animation:
            self.master.update()

        self.sound_board.chip_sound.play()
        self.update_text()

        if table_state['blackjack']:
            self.master.show_next_round_options()
            self.show_winner_text(table_state['has_winner'])
        else:
            self.master.show_gameplay_buttons()
            self.check_for_winner()

    def next_round(self):
        self.delete(self.winner_text)
        self.winner_text = None
        self.game_state.assign_winnings()
        if self.game_state.player_can_place_bet():
            self.game_state.next_round()
            self.display_table()
        else:
            self.show_out_of_money_text()
            self.master.on_game_over()

    def update_text(self):
        self.delete(self.player_money_text, self.player_score_text, self.pot_money_text)

        self.player_score_text = self.create_text(self.PLAYER_SCORE_TEXT_COORDS,
                                                  text=self.game_state.player_score_as_text(),
                                                  font=(None, 20))
        self.player_money_text = self.create_text(self.PLAYER_MONEY_COORDS, text=self.game_state.player_money_as_text(),
                                                  font=(None, 20))
        self.pot_money_text = self.create_text(self.POT_MONEY_COORDS, text=self.game_state.pot_money_as_text(),
                                               font=(None, 20))

    def show_winner_text(self, winner):
        if winner == 'p':
            self.winner_text = self.create_text(self.WINNER_TEXT_COORDS, text="YOU WIN!", font=(None, 50))
        elif winner == 'dp':
            self.winner_text = self.create_text(self.WINNER_TEXT_COORDS, text="TIE!", font=(None, 50))
        else:
            self.winner_text = self.create_text(self.WINNER_TEXT_COORDS, text="DEALER WINS!", font=(None, 50))

    def show_out_of_money_text(self):
        self.winner_text = self.create_text(self.WINNER_TEXT_COORDS, text="Out Of Money - Game Over", font=(None, 50))


class GameWindow(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Blackjack")
        self.geometry("800x640")
        self.resizable(False, False)

        self.bottom_frame = tk.Frame(self, width=800, height=140, bg="red")
        self.bottom_frame.pack_propagate(0)

        self.hit_button = tk.Button(self.bottom_frame, text="Hit", width=25, command=self.hit)
        self.stick_button = tk.Button(self.bottom_frame, text="Stick", width=25, command=self.stick)

        self.next_round_button = tk.Button(self.bottom_frame, text="Next Round", width=25, command=self.next_round)
        self.quit_button = tk.Button(self.bottom_frame, text="Quit", width=25, command=self.destroy)

        self.new_game_button = tk.Button(self.bottom_frame, text="New Game", width=25, command=self.new_game)

        self.bottom_frame.pack(side=tk.BOTTOM, fill=tk.X)

        self.game_screen = GameScreen(self, bg="white", width=800, height=500)
        self.game_screen.pack(side=tk.LEFT, anchor=tk.N)
        self.game_screen.setup_opening_animation()

    def on_winner(self):
        self.show_next_round_options()

    def on_game_over(self):
        self.hit_button.pack_forget()
        self.stick_button.pack_forget()
        self.new_game_button.pack(side=tk.LEFT, padx=(100, 200))
        self.quit_button.pack(side=tk.LEFT)

    def new_game(self):
        self.game_screen.refresh()
        self.game_screen.setup_opening_animation()
        self.remove_all_buttons()

    def remove_all_buttons(self):
        self.new_game_button.pack_forget()
        self.quit_button.pack_forget()

        self.hit_button.pack_forget()
        self.stick_button.pack_forget()

        self.next_round_button.pack_forget()

    def show_next_round_options(self):
        self.hit_button.pack_forget()
        self.stick_button.pack_forget()

        self.next_round_button.pack(side=tk.LEFT, padx=(100, 200))
        self.quit_button.pack(side=tk.LEFT)

    def show_gameplay_buttons(self):
        self.next_round_button.pack_forget()
        self.quit_button.pack_forget()

        self.hit_button.pack(side=tk.LEFT, padx=(100, 200))
        self.stick_button.pack(side=tk.LEFT)

    def next_round(self):
        self.remove_all_buttons()
        self.game_screen.next_round()

    def hit(self):
        self.game_screen.hit()

    def stick(self):
        self.game_screen.stick()


class GameState:
    def __init__(self):
        self.BASE_BET = 5
        self.minimum_bet = self.BASE_BET
        self.current_round = 1
        self.pot = 0

        self.deck = Deck()
        self.deck.shuffle()

        self.player = Player()
        self.dealer = Dealer()

        self.begin_round()

    def begin_round(self):
        self.has_winner = ''

        for i in range(2):
            self.player.receive_card(self.deck.deal())
            self.dealer.receive_card(self.deck.deal())

        self.player.place_bet(self.minimum_bet)
        self.add_bet(self.minimum_bet * 2)

    def player_can_place_bet(self):
        return self.player.can_place_bet(self.minimum_bet)

    def next_round(self):
        self.current_round += 1
        self.minimum_bet = self.BASE_BET * self.current_round

        self.player.empty_hand()
        self.dealer.empty_hand()

        self.begin_round()

    def add_bet(self, amount):
        self.pot += amount

    def assign_winnings(self):
        winner = self.has_winner
        if winner == 'p':
            self.player.add_winnings(self.pot)
            self.pot = 0
        elif winner == 'd':
            self.pot = 0

    def hit(self, card):
        self.player.receive_card(card)

    def draw(self):
        return self.deck.deal()

    def check_for_winner(self):
        if self.player.has_blackjack:
            self.has_winner = 'p'
        elif self.player.is_over:
            self.has_winner = 'd'

        return self.has_winner

    def get_table_state(self):
        blackjack = False
        winner = self.has_winner
        if not winner:
            winner = self.someone_has_blackjack()
            if winner:
                blackjack = True
        table_state = {
            'player_cards': self.player.cards,
            'dealer_cards': self.dealer.cards,
            'has_winner': winner,
            'blackjack': blackjack,
            'player_money': self.player.money
        }

        return table_state

    def calculate_final_state(self):
        player_hand_value = self.player.score
        dealer_hand_value = self.dealer.score

        if player_hand_value == dealer_hand_value:
            winner = 'dp'
        elif player_hand_value > dealer_hand_value:
            winner = 'p'
        else:
            winner = 'd'

        self.has_winner = winner

        table_state = {
            'player_cards': self.player.cards,
            'dealer_cards': self.dealer.cards,
            'has_winner': winner,
            'player_money': self.player.money
        }

        return table_state

    def player_score_as_text(self):
        return "Score: " + str(self.player.score)

    def player_money_as_text(self):
        return "Money: £" + str(self.player.money)

    def pot_money_as_text(self):
        return "Pot: £" + str(self.pot)

    def someone_has_blackjack(self):
        player = False
        dealer = False
        if self.player.has_blackjack:
            player = True
        if self.dealer.has_blackjack:
            dealer = True

        if player and dealer:
            return 'dp'
        elif player:
            return 'p'
        elif dealer:
            return 'd'

        return False


if __name__ == "__main__":
    gw = GameWindow()
    gw.mainloop()
