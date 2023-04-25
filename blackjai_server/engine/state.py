
# Contains the global state holding the count, the number and type of cards dealt, and the current game state (e.g. betting, playing, etc.)

class BlackJAIState:
    def __init__(self):
        self.count = 0
        self.cards = []
        self.game_state = "betting"

    def update_count(self, card):
        if card in ["2", "3", "4", "5", "6"]:
            self.count += 1
        elif card in ["10", "J", "Q", "K", "A"]:
            self.count -= 1

    def update_cards(self, card):
        self.cards.append(card)

    def update_game_state(self, game_state):
        self.game_state = game_state

    def reset(self):
        self.count = 0
        self.cards = []
        self.game_state = "betting"

