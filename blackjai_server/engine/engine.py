from .state import BlackJAIState

class BlackJAIEngine:
    def __init__(self):
        self.state = BlackJAIState()

    def update(self, image_data):
        # TODO: Break image into 3 sections. One for each player and one for the dealer.
        
        # TODO: Use the image data to update the state of the game.