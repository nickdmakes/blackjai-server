import re

# Contains the model for the counting system (Hi-Lo) for the game of blackjack

# A card class that holds the value and suit of a card

DEBUG = True

class Card:
    def __init__(self, value_suit: str):
        str_len = len(value_suit)
        self.value = str(value_suit[0])
        self.suit = str(value_suit[1:str_len])
        # Check if the card is a 10
        if (str_len > 2):
            self.value = str(value_suit[0:2])
            self.suit = str(value_suit[str_len-1])

    def get_value(self):
        if (self.value in ["J", "Q", "K"]):
            return 10
        elif (self.value == "A"):
            return 11
        else:
            return int(self.value)

    def get_suit(self):
        return self.suit

    def set_value(self, value: str):
        self.value = value

    def set_suit(self, suit: str):
        self.suit = suit

    def __str__(self):
        return str(self.value) + " of " + str(self.suit)


# A player class that holds the player's hand which contains a set of cards, the player's minimum bet, and the player's current balance
class Player:
    def __init__(self, minimum_bet, balance):
        self.hands = []
        self.minimum_bet = minimum_bet
        self.balance = balance

    def get_num_hands(self):
        return len(self.hands)

    def get_hands(self) -> list[list[Card]]:
        return self.hands

    def get_hand(self, hand_index: int) -> list[Card]:
        if (hand_index >= len(self.hands)):
            raise Exception("Hand index out of range")
        return self.hands[hand_index]

    def get_minimum_bet(self):
        return self.minimum_bet

    def get_balance(self):
        return self.balance

    def add_hand(self, hand: list[Card]):
        if (len(self.hands) == 0):
            self.hands = [hand]
        else:
            self.hands.append(hand)

    def add_card_to_hand(self, hand_index: int, card: Card):
        if (hand_index >= len(self.hands)):
            raise Exception("Hand index out of range")
        self.hands[hand_index].append(card)

    def remove_hand(self, hand_index: int):
        if (hand_index >= len(self.hands)):
            raise Exception("Hand index out of range")
        self.hands.pop(hand_index)

    def reset_hands(self):
        self.hands = []

    def update_balance(self, amount):
        self.balance += amount

    def __str__(self):
        return "Cards: " + str(self.hands) + "\nMinimum Bet: " + str(self.minimum_bet) + "\nBalance: " + str(self.balance)


# The model for the optimal strategy for the game of blackjack (basic strategy)
class BasicStrategy:
    # Define each action key for the basic strategy
    H_ = "H"
    S_ = "S"
    DH = "DH"
    DS = "DS"
    RH = "RH"
    P_ = "P"
    PH = "PH"
    PD = "PD"
    RS = "RS"

    # Map each action key to its corresponding action description
    ACTIONS = {H_: "Hit", S_: "Stand", DH: "Double down if permitted, else Hit", DS: "Double down if permitted, else Stand",
               RH: "Surrender if permitted, else Hit", P_: "Split", PH: "Split if double down permitted, else Hit",
               PD: "Split if double down permitted, else Double down", RS: "Surrender if permitted, else Stand"}

    # Define the dealer's up card index offset
    DEALER_OFFSET = 2

    # Dealer's up card on rows starting from 2 to A (including 10) [0:9]
    # Player's hand on columns starting from 7 to 17 (Anything below a 7 is a Hit (H_). Anything above 17 is a Stand (S_).) [0:10]
    BASIC_STRATEGY_HARD = [
        #          2,           3,           4,           5,           6,           7,           8,           9,          10,           A
        [ACTIONS[H_], ACTIONS[H_], ACTIONS[H_], ACTIONS[H_], ACTIONS[H_], ACTIONS[H_], ACTIONS[H_], ACTIONS[H_], ACTIONS[H_], ACTIONS[H_]],  # 7 or less
        [ACTIONS[H_], ACTIONS[H_], ACTIONS[H_], ACTIONS[DH], ACTIONS[DH], ACTIONS[H_], ACTIONS[H_], ACTIONS[H_], ACTIONS[H_], ACTIONS[H_]],  # 8
        [ACTIONS[DH], ACTIONS[DH], ACTIONS[DH], ACTIONS[DH], ACTIONS[DH], ACTIONS[DH], ACTIONS[H_], ACTIONS[H_], ACTIONS[H_], ACTIONS[H_]],  # 9
        [ACTIONS[DH], ACTIONS[DH], ACTIONS[DH], ACTIONS[DH], ACTIONS[DH], ACTIONS[DH], ACTIONS[DH], ACTIONS[DH], ACTIONS[H_], ACTIONS[H_]],  # 10
        [ACTIONS[DH], ACTIONS[DH], ACTIONS[DH], ACTIONS[DH], ACTIONS[DH], ACTIONS[DH], ACTIONS[DH], ACTIONS[DH], ACTIONS[DH], ACTIONS[DH]],  # 11
        [ACTIONS[H_], ACTIONS[H_], ACTIONS[S_], ACTIONS[S_], ACTIONS[S_], ACTIONS[H_], ACTIONS[H_], ACTIONS[H_], ACTIONS[H_], ACTIONS[H_]],  # 12
        [ACTIONS[S_], ACTIONS[S_], ACTIONS[S_], ACTIONS[S_], ACTIONS[S_], ACTIONS[H_], ACTIONS[H_], ACTIONS[H_], ACTIONS[H_], ACTIONS[H_]],  # 13
        [ACTIONS[S_], ACTIONS[S_], ACTIONS[S_], ACTIONS[S_], ACTIONS[S_], ACTIONS[H_], ACTIONS[H_], ACTIONS[H_], ACTIONS[H_], ACTIONS[H_]],  # 14
        [ACTIONS[S_], ACTIONS[S_], ACTIONS[S_], ACTIONS[S_], ACTIONS[S_], ACTIONS[H_], ACTIONS[H_], ACTIONS[H_], ACTIONS[H_], ACTIONS[H_]],  # 15
        [ACTIONS[S_], ACTIONS[S_], ACTIONS[S_], ACTIONS[S_], ACTIONS[S_], ACTIONS[H_], ACTIONS[H_], ACTIONS[H_], ACTIONS[RH], ACTIONS[RH]],  # 16
        [ACTIONS[S_], ACTIONS[S_], ACTIONS[S_], ACTIONS[S_], ACTIONS[S_], ACTIONS[S_], ACTIONS[S_], ACTIONS[S_], ACTIONS[S_], ACTIONS[S_]]   # 17 or more
    ]

    # Dealer's up card on rows starting from 2 to A (including 10) [0:9]
    # Player's hand on columns starting from 13 to 21 (Anything below a 13 is a Hit (H_).) [0:8]
    BASIC_STRATEGY_SOFT = [
        #          2,           3,           4,           5,           6,           7,           8,           9,          10,           A
        [ACTIONS[H_], ACTIONS[H_], ACTIONS[DH], ACTIONS[DH], ACTIONS[DH], ACTIONS[H_], ACTIONS[H_], ACTIONS[H_], ACTIONS[H_], ACTIONS[H_]],  # 13
        [ACTIONS[H_], ACTIONS[H_], ACTIONS[DH], ACTIONS[DH], ACTIONS[DH], ACTIONS[H_], ACTIONS[H_], ACTIONS[H_], ACTIONS[H_], ACTIONS[H_]],  # 14
        [ACTIONS[H_], ACTIONS[H_], ACTIONS[DH], ACTIONS[DH], ACTIONS[DH], ACTIONS[H_], ACTIONS[H_], ACTIONS[H_], ACTIONS[H_], ACTIONS[H_]],  # 15
        [ACTIONS[H_], ACTIONS[H_], ACTIONS[DH], ACTIONS[DH], ACTIONS[DH], ACTIONS[H_], ACTIONS[H_], ACTIONS[H_], ACTIONS[H_], ACTIONS[H_]],  # 16
        [ACTIONS[DH], ACTIONS[DH], ACTIONS[DH], ACTIONS[DH], ACTIONS[DH], ACTIONS[H_], ACTIONS[H_], ACTIONS[H_], ACTIONS[H_], ACTIONS[H_]],  # 17
        [ACTIONS[S_], ACTIONS[DS], ACTIONS[DS], ACTIONS[DS], ACTIONS[DS], ACTIONS[S_], ACTIONS[S_], ACTIONS[H_], ACTIONS[H_], ACTIONS[S_]],  # 18
        [ACTIONS[S_], ACTIONS[S_], ACTIONS[S_], ACTIONS[S_], ACTIONS[DS], ACTIONS[S_], ACTIONS[S_], ACTIONS[S_], ACTIONS[S_], ACTIONS[S_]],  # 19
        [ACTIONS[S_], ACTIONS[S_], ACTIONS[S_], ACTIONS[S_], ACTIONS[S_], ACTIONS[S_], ACTIONS[S_], ACTIONS[S_], ACTIONS[S_], ACTIONS[S_]],  # 20
        [ACTIONS[S_], ACTIONS[S_], ACTIONS[S_], ACTIONS[S_], ACTIONS[S_], ACTIONS[S_], ACTIONS[S_], ACTIONS[S_], ACTIONS[S_], ACTIONS[S_]]   # 21
    ]

    # Dealer's up card on rows starting from 2 to A (including 10) [0:9]
    # Player's hand on columns starting from (2,2), (3,3), etc. to (A,A) (including 10) [0:9]
    BASIC_STRATEGY_PAIRS = [
        #          2,           3,           4,           5,           6,           7,           8,           9,          10,           A
        [ACTIONS[PH], ACTIONS[P_], ACTIONS[P_], ACTIONS[P_], ACTIONS[P_], ACTIONS[P_], ACTIONS[H_], ACTIONS[H_], ACTIONS[H_], ACTIONS[H_]],  # 2,2
        [ACTIONS[PH], ACTIONS[PH], ACTIONS[P_], ACTIONS[P_], ACTIONS[P_], ACTIONS[P_], ACTIONS[PH], ACTIONS[H_], ACTIONS[H_], ACTIONS[H_]],  # 3,3
        [ACTIONS[H_], ACTIONS[H_], ACTIONS[PH], ACTIONS[PD], ACTIONS[PD], ACTIONS[H_], ACTIONS[H_], ACTIONS[H_], ACTIONS[H_], ACTIONS[H_]],  # 4,4
        [ACTIONS[DH], ACTIONS[DH], ACTIONS[DH], ACTIONS[DH], ACTIONS[DH], ACTIONS[DH], ACTIONS[DH], ACTIONS[DH], ACTIONS[H_], ACTIONS[H_]],  # 5,5
        [ACTIONS[P_], ACTIONS[P_], ACTIONS[P_], ACTIONS[P_], ACTIONS[P_], ACTIONS[PH], ACTIONS[H_], ACTIONS[H_], ACTIONS[H_], ACTIONS[H_]],  # 6,6
        [ACTIONS[P_], ACTIONS[P_], ACTIONS[P_], ACTIONS[P_], ACTIONS[P_], ACTIONS[P_], ACTIONS[PH], ACTIONS[H_], ACTIONS[RS], ACTIONS[H_]],  # 7,7
        [ACTIONS[P_], ACTIONS[P_], ACTIONS[P_], ACTIONS[P_], ACTIONS[P_], ACTIONS[P_], ACTIONS[P_], ACTIONS[P_], ACTIONS[P_], ACTIONS[P_]],  # 8,8
        [ACTIONS[P_], ACTIONS[P_], ACTIONS[P_], ACTIONS[P_], ACTIONS[P_], ACTIONS[S_], ACTIONS[P_], ACTIONS[P_], ACTIONS[S_], ACTIONS[S_]],  # 9,9
        [ACTIONS[S_], ACTIONS[S_], ACTIONS[S_], ACTIONS[S_], ACTIONS[S_], ACTIONS[S_], ACTIONS[S_], ACTIONS[S_], ACTIONS[S_], ACTIONS[S_]],  # 10,10
        [ACTIONS[P_], ACTIONS[P_], ACTIONS[P_], ACTIONS[P_], ACTIONS[P_], ACTIONS[P_], ACTIONS[P_], ACTIONS[P_], ACTIONS[P_], ACTIONS[P_]]   # A,A
    ]

    def __init__(self):
        # create a lookup table for the basic strategy
        pass

    # returns the sum of the cards in a tuple (sum, is_soft)
    def sum_cards(self, cards: list[Card]) -> tuple[int, bool]:
        ace_high_count = 0
        sum = 0
        for card in cards:
            cur_val = card.get_value()
            if ((cur_val == 11) and ((sum + cur_val) > 21)):
                sum += 1
            elif (cur_val == 11):
                sum += cur_val
                ace_high_count += 1
            else:
                sum += cur_val
            # check if we need to convert an ace from high to low
            if ((sum > 21) and (ace_high_count > 0)):
                sum -= 10
                ace_high_count -= 1
        return (sum, ace_high_count > 0)

    def get_action(self, player: Player, dealer_card: Card) -> str:
        # TODO handle split hands after split is done...

        hands = player.get_hands()
        hand0_cards = hands[0]
        num_cards = len(hand0_cards)

        # get the sum of the player's cards and determine if it's a soft hand
        cards_sum, is_soft = self.sum_cards(hand0_cards)

        if (cards_sum > 21):
            return "Bust"
        elif ((cards_sum == 21) and (num_cards == 2)):
            return "Blackjack!"
        else:
            dealer_idx = dealer_card.get_value() - self.DEALER_OFFSET
            # determine if hard or soft hand or if pair
            if (num_cards == 2 and (hand0_cards[0].get_value() == hand0_cards[1].get_value())):
                # pair
                PLAYER_OFFSET = 2
                player_idx = hand0_cards[0].get_value() - PLAYER_OFFSET
                return self.BASIC_STRATEGY_PAIRS[dealer_idx][player_idx]
            elif (num_cards == 2 and is_soft):
                # soft hand
                PLAYER_OFFSET = 13
                player_idx = cards_sum - PLAYER_OFFSET
                return self.BASIC_STRATEGY_SOFT[dealer_idx][player_idx]
            elif (num_cards == 2):
                # hard hand
                PLAYER_OFFSET = 7
                player_idx = cards_sum - PLAYER_OFFSET
                # check if player has less than a 7 hand
                if (player_idx < 0):
                    # will always hit
                    player_idx = 0

                # check is player has more than a 17 hand
                if (player_idx > 10):
                    # will always stand
                    player_idx = 10

                return self.BASIC_STRATEGY_HARD[dealer_idx][player_idx]
            elif (num_cards > 2):
                # TODO handle 2+ cards in player's hand
                print("TODO: handle 2+ cards in player's hand")
                pass


def test1():
    dealer = Card("KS")
    player1 = Player(1, 10)
    player2 = Player(1, 10)

    player1_hand1 = [Card("2H"), Card("10D")]
    player2_hand1 = [Card("5C"), Card("AH")]

    player1.add_hand(player1_hand1)
    player2.add_hand(player2_hand1)

    bs = BasicStrategy()
    print(bs.get_action(player1, dealer))
    print(bs.get_action(player2, dealer))


if __name__ == "__main__":
    # test the models
    test1()
    
    print("Done")
