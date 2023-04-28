import math

"""
Contains all the model used in the game of blackjack and for the BlackJAI system
"""

# A card class that holds the value and suit of a card
class Card:
    def __init__(self, value_suit: str):
        str_len = len(value_suit)
        if (str_len < 2):
            raise Exception("Card value and suit must be at least 2 characters long")
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

    def get_value_suit(self):
        return self.value + self.suit

    def set_value(self, value: str):
        self.value = value

    def set_suit(self, suit: str):
        self.suit = suit

    def __str__(self):
        return self.get_value_suit()

    def __repr__(self) -> str:
        return self.get_value_suit()


# A class for the queue object. Contains a tuple of: (card location, card, confidence level)
# Frames will output multiple of these objects
class CardInfo:
    def __init__(self, location: tuple[int, int], card: Card, confidence):
        self.location = location
        self.card = card
        self.confidence = confidence

    def get_location(self) -> tuple[int, int]:
        return self.location

    def get_card(self) -> Card:
        return self.card

    def get_confidence(self):
        return self.confidence

    def set_location(self, location: tuple[int, int]):
        self.location = location

    def set_card(self, card: Card):
        self.card = card

    def set_confidence(self, confidence):
        self.confidence = confidence

    # returns the location difference between this card and another card
    def get_loc_diff(self, card_info):
        return int(math.sqrt((self.location[0] - card_info.get_location()[0])**2 + (self.location[1] - card_info.get_location()[1])**2))

    # returns the average location and confidence between this card and another card (must be the same card)
    def avg_card_infos(self, card_info):
        if (self.card.get_value_suit() != card_info.card.get_value_suit()):
            raise Exception("CardInfo objects must be the same card")
        return CardInfo((int((self.location[0] + card_info.location[0]) / 2),
                         int((self.location[1] + card_info.location[1]) / 2)),
                        self.card, (self.confidence + card_info.confidence) / 2)

    def __str__(self):
        return "(" + str(self.location) + " " + str(self.card) + " " + str(self.confidence) + ")"

    def __repr__(self):
        return "(" + str(self.location) + " " + str(self.card) + " " + str(self.confidence) + ")"


# A player class that holds the player's hand which contains a set of cards, the player's minimum bet
class Player:
    def __init__(self, minimum_bet=1):
        self.hands = []
        self.minimum_bet = minimum_bet

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

    # Returns tuple of (hand index, card index) if card is in hand, else returns None
    def is_card_in_hands(self, card: Card):
        for i in range(len(self.hands)):
            hand = self.hands[i]
            for j in range(len(hand)):
                c = hand[j]
                if (c.get_value_suit() == card.get_value_suit()):
                    return (i, j)
        return None

    # Check if the player has a hand that contains the same cards as the other hand
    def conatins_hand(self, other_hand: list[CardInfo]):
        hand_match = False
        for hand in self.hands:
            for card in hand:
                if ((len(hand) != len(other_hand)) or not all(card.get_value_suit() == other_card.get_card().get_value_suit() for other_card in other_hand)):
                    hand_match = False
                    break
                else:
                    hand_match = True
            if (hand_match):
                break
        return hand_match

    def add_hand(self, hand: list[Card]):
        if (len(self.hands) == 0):
            self.hands = [hand]
        else:
            self.hands.append(hand)

    def add_card_to_hand(self, hand_index: int, card: Card):
        if (hand_index >= len(self.hands)):
            raise Exception("Hand index out of range")
        self.hands[hand_index].append(card)

    def split_cards_in_hand(self, hand_index: int):
        if (hand_index >= len(self.hands)):
            raise Exception("Hand index out of range")
        if (len(self.hands[hand_index]) != 2):
            raise Exception("Hand does not contain 2 cards")
        if (self.hands[hand_index][0].get_value() != self.hands[hand_index][1].get_value()):
            raise Exception("Cards in hand are not the same value")
        card = self.hands[hand_index].pop()
        self.add_hand([card])

    def remove_hand(self, hand_index: int):
        if (hand_index >= len(self.hands)):
            raise Exception("Hand index out of range")
        self.hands.pop(hand_index)

    def remove_card_from_hand(self, hand_index: int, card_index: int):
        if (hand_index >= len(self.hands)):
            raise Exception("Hand index out of range")
        if (card_index >= len(self.hands[hand_index])):
            raise Exception("Card index out of range")
        self.hands[hand_index].pop(card_index)

    def reset_hands(self):
        self.hands = []

    def __str__(self):
        return "Cards: " + str(self.hands) + "\nMinimum Bet: " + str(self.minimum_bet)

    def __repr__(self) -> str:
        return "Cards: " + str(self.hands) + "\nMinimum Bet: " + str(self.minimum_bet)

    # Serialize the player object to a dictionary
    def serialize(self):
        return {"hands": [self.serialize_hand(hand) for hand in self.hands], "minimum_bet": self.minimum_bet}

    def serialize_hand(self, hand: list[Card]):
        return [card.get_value_suit() for card in hand]


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
    # custom actions
    BJ = "BJ"
    BS = "BS"
    ER = "ER"

    # Map each action key to its corresponding action description
    ACTIONS_TEXT = {H_: "Hit", S_: "Stand", DH: "Double down if permitted, else Hit", DS: "Double down if permitted, else Stand",
                    RH: "Surrender if permitted, else Hit", P_: "Split", PH: "Split if double down permitted, else Hit",
                    PD: "Split if double down permitted, else Double down", RS: "Surrender if permitted, else Stand", BJ: "Blackjack",
                    BS: "Bust", ER: "Error: Soft hand over 21"}

    ACTIONS = {H_: H_, S_: S_, DH: DH, DS: DS, RH: RH, P_: P_, PH: PH, PD: PD, RS: RS, BJ: BJ, BS: BS, ER: ER}

    # Define the dealer's up card index offset
    DEALER_OFFSET = 2

    # Dealer's up card per column starting from 2 to A (including 10) [0:9]
    # Player's hand per row starting from 7 to 17 (Anything below a 7 is a Hit (H_). Anything above 17 is a Stand (S_).) [0:10]
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

    # Dealer's up card per column starting from 2 to A (including 10) [0:9]
    # Player's hand per row starting from 13 to 21 (Anything below a 13 is a Hit (H_).) [0:8]
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

    # Dealer's up card per column starting from 2 to A (including 10) [0:9]
    # Player's hand per row starting from (2,2), (3,3), etc. to (A,A) (including 10) [0:9]
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

    # returns a list of actions to take for each hand
    def get_action(self, player: Player, dealer_card: Card) -> list[str]:
        actions_list = []
        # handle split cards by iterating through each hand and getting the action
        for i in range(player.get_num_hands()):
            cur_hand = player.get_hand(i)
            num_cards = len(cur_hand)
            dealer_idx = dealer_card.get_value() - self.DEALER_OFFSET

            # get the sum of the player's cards and determine if it's a soft hand
            cards_sum, is_soft = self.sum_cards(cur_hand)

            if (cards_sum > 21):
                if (is_soft):
                    actions_list.append(self.ER)
                else:
                    actions_list.append(self.BS)
            elif ((cards_sum == 21) and (num_cards == 2)):
                actions_list.append(self.BJ)
            elif ((num_cards == 2) and (cur_hand[0].get_value() == cur_hand[1].get_value())):
                # pair
                PLAYER_OFFSET = 2
                player_idx = cur_hand[0].get_value() - PLAYER_OFFSET
                actions_list.append(self.BASIC_STRATEGY_PAIRS[player_idx][dealer_idx])
            elif ((num_cards >= 2) and is_soft):
                # soft hand
                PLAYER_OFFSET = 13
                player_idx = cards_sum - PLAYER_OFFSET
                actions_list.append(self.BASIC_STRATEGY_SOFT[player_idx][dealer_idx])
            elif (num_cards >= 2):
                # hard hand
                PLAYER_OFFSET = 7
                player_idx = cards_sum - PLAYER_OFFSET
                if (player_idx < 0):
                    # if player has less than a 7 hand, always hit
                    player_idx = 0
                if (player_idx > 10):
                    # if player has more than a 17 hand, always stand
                    player_idx = 10
                actions_list.append(self.BASIC_STRATEGY_HARD[player_idx][dealer_idx])
            else:
                # only one card, always hit
                actions_list.append(self.H_)
        return actions_list


# The model for the counting systems (Hi-Lo, Omega II, Wong Halves, Zen Count) for the game of blackjack
class CountingSystems:
    def __init__(self, num_decks=1):
        self.num_decks = num_decks
        self.deck_dict = {}
        self.count_hi_lo = 0
        self.count_omega_ii = 0
        self.count_wong_halves = 0
        self.count_zen_count = 0

    def get_true_count_hi_lo(self, num_decks_remaining) -> float:
        return self.count_hi_lo / num_decks_remaining

    def get_true_count_omega_ii(self, num_decks_remaining) -> float:
        return self.count_omega_ii / num_decks_remaining

    def get_true_count_wong_halves(self, num_decks_remaining) -> float:
        return self.count_wong_halves / num_decks_remaining

    def get_true_count_zen_count(self, num_decks_remaining) -> float:
        return self.count_zen_count / num_decks_remaining

    def get_bet_multiplier_hi_lo(self, num_decks_remaining) -> float:
        true_count = self.get_true_count_hi_lo(num_decks_remaining)
        return max(1, true_count)

    def get_bet_multiplier_omega_ii(self, num_decks_remaining) -> float:
        true_count = self.get_true_count_omega_ii(num_decks_remaining)
        return max(1, true_count)

    def get_bet_multiplier_wong_halves(self, num_decks_remaining) -> float:
        true_count = self.get_true_count_wong_halves(num_decks_remaining)
        return max(1, true_count)

    def get_bet_multiplier_zen_count(self, num_decks_remaining) -> float:
        true_count = self.get_true_count_zen_count(num_decks_remaining)
        return max(1, true_count)

    def set_num_decks(self, num_decks: int):
        self.num_decks = num_decks

    # update all running counts for the card(s) in the hand if they have not been seen before
    # or if there are less than the number of decks
    def update_running_counts_hand(self, hand: list[Card]):
        for card in hand:
            self.update_running_counts_card(card)

    # update all running counts if the card has not been seen before or if there are less than the number of decks
    def update_running_counts_card(self, card: Card):
        # add card to deck dictionary if it doesn't exist
        update_count = False
        if (card.get_value_suit() not in self.deck_dict):
            self.deck_dict[card.get_value_suit()] = 1
            update_count = True
        elif (self.deck_dict[card.get_value_suit()] < self.num_decks):
            self.deck_dict[card.get_value_suit()] += 1
            update_count = True
        if (update_count):
            card_val = card.get_value()
            # Hi-Lo
            if (card_val <= 6):
                self.count_hi_lo += 1
            elif (card_val >= 10):
                self.count_hi_lo -= 1

            # Omega II
            if (card_val == 2 or card_val == 3 or card_val == 7):
                self.count_omega_ii += 1
            elif (card_val >= 4 and card_val <= 6):
                self.count_omega_ii += 2
            elif (card_val == 9):
                self.count_omega_ii -= 1
            elif (card_val == 10):
                self.count_omega_ii -= 2

            # Wong Halves
            if (card_val == 2 or card_val == 7):
                self.count_wong_halves += 0.5
            elif (card_val == 3 or card_val == 4 or card_val == 6):
                self.count_wong_halves += 1
            elif (card_val == 5):
                self.count_wong_halves += 1.5
            elif (card_val == 9):
                self.count_wong_halves -= 0.5
            elif (card_val == 10 or card_val == 11):
                self.count_wong_halves -= 1

            # Zen Count
            if (card_val == 2 or card_val == 3 or card_val == 7):
                self.count_zen_count += 1
            elif (card_val >= 4 and card_val <= 6):
                self.count_zen_count += 2
            elif (card_val == 10):
                self.count_zen_count -= 2
            elif (card_val == 11):
                self.count_zen_count -= 1

    def reset_running_counts(self):
        self.count_hi_lo = 0
        self.count_omega_ii = 0
        self.count_wong_halves = 0
        self.count_zen_count = 0
        self.deck_dict = {}

    def __str__(self) -> str:
        return "Hi-Lo: " + str(self.count_hi_lo) + "\nOmega II: " + str(self.count_omega_ii) + \
               "\nWong Halves: " + str(self.count_wong_halves) + "\nZen Count: " + str(self.count_zen_count)

    # serialize the running counts
    def serialize(self) -> dict:
        return {
            "count_hi_lo": self.count_hi_lo,
            "count_omega_ii": self.count_omega_ii,
            "count_wong_halves": self.count_wong_halves,
            "count_zen_count": self.count_zen_count,
            "deck_dict": self.deck_dict
        }


def test1(bs: BasicStrategy):
    dealer = Card("KS")
    player1 = Player(1)
    player2 = Player(1)

    player1_hand1 = [Card("2H"), Card("10D")]
    player2_hand1 = [Card("5C"), Card("AH")]

    player1.add_hand(player1_hand1)
    player2.add_hand(player2_hand1)

    print(bs.get_action(player1, dealer))
    print(bs.get_action(player2, dealer))


if __name__ == "__main__":
    # test the models
    bs = BasicStrategy()
    test1(bs)
    print("Done")
