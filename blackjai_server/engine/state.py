# State object for the game engine

# import the player class
from blackjai_server.engine.models import Player, Card, CountingSystems

# Phases of the game
SHUFFLE_PHASE = "shuffle"
DEAL_PHASE = "deal"
TURN_PHASE = "turn"


class BlackJAIState:
    def __init__(self, num_players=2):
        self.phase = "shuffle"
        self.players = []
        for i in range(num_players):
            self.players.append(Player(minimum_bet=5))
        self.dealer = Player(minimum_bet=0)
        self.count_systems = CountingSystems(num_decks=1)

    def get_phase(self) -> str:
        return self.phase

    def get_num_players(self) -> int:
        return len(self.players)

    def get_players(self) -> list[Player]:
        return self.players

    def get_player(self, index) -> Player:
        return self.players[index]

    def get_dealer(self) -> Player:
        return self.dealer

    def get_count_systems(self) -> CountingSystems:
        return self.count_systems

    def set_phase(self, phase):
        self.phase = phase

    def set_player(self, player_index: int, player: Player):
        self.players[player_index] = player

    # Adds a hand (list of cards) to a player
    def add_hand_to_player(self, player_index: int, cards: list[Card]):
        self.players[player_index].add_hand(cards)

    # Adds a card to a player's hand
    def add_card_to_player_hand(self, player_index: int, hand_index: int, card: Card):
        self.players[player_index].add_card_to_hand(hand_index, card)

    # Adds a hand (list of cards) to the dealer
    def add_hand_to_dealer(self, cards: list[Card]):
        self.dealer.add_hand(cards)

    # Adds a card to the dealer's hand
    def add_card_to_dealer(self, card: Card):
        self.dealer.add_card_to_hand(0, card)

    def reset_player_hands(self):
        for player in self.players:
            player.reset_hands()

    def reset_state(self):
        self.phase = "shuffle"
        self.reset_player_hands()
        self.dealer.reset_hands()
