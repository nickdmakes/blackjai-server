# State object for the game engine

# import the player class
from blackjai_server.engine.models import Player, Card, CountingSystems

# Phases of the game
SHUFFLE_PHASE = "shuffle"
DEAL_PHASE = "deal"
TURN_PHASE = "turn"


class BlackJAIState:
    def __init__(self):
        self.phase = "shuffle"
        self.player_one = Player(minimum_bet=5)
        self.player_two = Player(minimum_bet=5)
        self.dealer_card = None
        self.count_systems = CountingSystems(num_decks=1)
        