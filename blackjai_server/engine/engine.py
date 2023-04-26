import sys

from state import BlackJAIState, SHUFFLE_PHASE, DEAL_PHASE, TURN_PHASE
from models import Card, CardInfo

DEBUG = True


class BlackJAIEngine:
    def __init__(self, num_players=2, buffer_size=20, thresh_same_card=250, thresh_card_moving=150, thresh_card_cluster=400):
        self.num_players = num_players
        self.state = BlackJAIState(num_players)
        self.buffer_size = buffer_size
        # threshold for card location difference to determine if 2 card labels are the same
        self.thresh_same_card = thresh_same_card
        # threshold for card location difference to determine if 1 card is moving
        self.thresh_card_moving = thresh_card_moving
        self.thresh_card_cluster = thresh_card_cluster
        self.frame_card_info_queues = CardInfoQueues(buffer_size)

    def update(self, json_data):
        self._update_card_info_queues(json_data)
        # handle state changes
        if (self.state.get_phase() == SHUFFLE_PHASE):
            if (not self.frame_card_info_queues.is_empty()):
                self.state.set_phase(DEAL_PHASE)
                print("Shuffle phase complete. Deal phase started.") if DEBUG else None
        elif (self.state.get_phase() == DEAL_PHASE):
            # determine when 5 distinct cards are not moving anymore
            avg_card_locs = self.frame_card_info_queues.get_avg_locs(self.thresh_card_moving)
            if (len(avg_card_locs) >= (self.num_players * 2 + 1)):
                # segment cards into number of players + dealer piles
                hands = self._cluster_cards(avg_card_locs)
                player_num = 0
                for i in range(len(hands)):
                    hand = hands[i]
                    if (len(hand) == 2):
                        self.state.add_hand_to_player(player_num, hand)
                        player_num += 1
                    elif (len(hand) == 1):
                        self.state.set_dealer_card(hand[0].get_card())
                    else:
                        print("ERROR: hand has more than 2 cards. In BlackJAIEngine.update()")
                self.state.set_phase(TURN_PHASE)
                print("Deal phase complete. Turn phase started.") if DEBUG else None
        elif (self.state.get_phase() == TURN_PHASE):
            # TODO 
            pass
        else:
            # nothing (error)
            pass

    # Clusters the cards into piles for each player and the dealer.
    # Returns a 2D list of CardInfo where each row is a player's or dealer's hand.
    def _cluster_cards(self, card_loc_dict: dict[str, tuple[int, int]]) -> list[list[CardInfo]]:
        hands = []
        for key in card_loc_dict.keys():
            appended = False
            card_location = card_loc_dict[key]
            # check if card is close enough to any of the hands
            for i in range(len(hands)):
                hand = hands[i]
                # check if card is close enough to any of the cards in the hand
                for j in range(len(hand)):
                    card_info = hand[j]
                    if (self._get_loc_diff(card_info.get_location(), card_location) < self.thresh_card_cluster):
                        # add card to hand
                        hand.append(CardInfo(card_location, Card(key), 1))
                        appended = True
                        break
            # if not close enough or did not enter for loop, add card to new hand
            if (not appended):
                hands.append([CardInfo(card_location, Card(key), 1)])
        if (len(hands) != self.num_players + 1):
            print("ERROR: number of hands does not match number of players + 1 (dealer). In BlackJAIEngine._cluster_cards()")
        return hands

    # returns the location difference between 2 locations
    def _get_loc_diff(self, loc1: tuple[int, int], loc2: tuple[int, int]):
        return abs(loc1[0] - loc2[0]) + abs(loc1[1] - loc2[1])

    def _update_card_info_queues(self, json_data):
        card_dict = {}
        if json_data["predictions"]:
            for prediction in json_data["predictions"]:
                # get the bounding box of the prediction
                x1 = int(prediction["x"])
                y1 = int(prediction["y"])
                x2 = int(x1 + prediction["width"])
                y2 = int(y1 + prediction["height"])

                # get prediction info
                card_type = prediction["class"]
                confidence = prediction["confidence"]
                cur_card_info = CardInfo((x1, y1), Card(card_type), confidence)
                # add card info as list to card_dict
                if (card_type not in card_dict):
                    card_dict[card_type] = [cur_card_info]
                else:
                    card_dict[card_type].append(cur_card_info)
        # find same cards labeled multiple times in card_dict
        # average their coordinates and confidence to get 1 card label per card type (key) in card_dict
        for card_info_list in card_dict.values():
            if (len(card_info_list) > 1):
                # find card labels that are close enough
                for i in range(len(card_info_list)):
                    for j in range(i + 1, len(card_info_list)):
                        if (card_info_list[i].get_loc_diff(card_info_list[j]) < self.thresh_same_card):
                            # average coordinates and confidence
                            card_info_list[i] = card_info_list[i].avg_card_infos(card_info_list[j])
                            # remove the card that was averaged
                            card_info_list.pop(j)
                            j -= 1
        self.frame_card_info_queues.add(card_dict)


# A dictionary class with keys as playing cards and values as a queue of CardInfo objects
class CardInfoQueues:
    # threshold for number of card infos in the queue for a card type
    THRESH_NUM_CARD_INFOS = 3

    def __init__(self, buffer_size=20):
        self.buffer_size = buffer_size
        self.dict = {
            # 2
            "2C": [],
            "2D": [],
            "2H": [],
            "2S": [],
            # 3
            "3C": [],
            "3D": [],
            "3H": [],
            "3S": [],
            # 4
            "4C": [],
            "4D": [],
            "4H": [],
            "4S": [],
            # 5
            "5C": [],
            "5D": [],
            "5H": [],
            "5S": [],
            # 6
            "6C": [],
            "6D": [],
            "6H": [],
            "6S": [],
            # 7
            "7C": [],
            "7D": [],
            "7H": [],
            "7S": [],
            # 8
            "8C": [],
            "8D": [],
            "8H": [],
            "8S": [],
            # 9
            "9C": [],
            "9D": [],
            "9H": [],
            "9S": [],
            # 10
            "10C": [],
            "10D": [],
            "10H": [],
            "10S": [],
            # J
            "JC": [],
            "JD": [],
            "JH": [],
            "JS": [],
            # Q
            "QC": [],
            "QD": [],
            "QH": [],
            "QS": [],
            # K
            "KC": [],
            "KD": [],
            "KH": [],
            "KS": [],
            # A
            "AC": [],
            "AD": [],
            "AH": [],
            "AS": [],
        }

    # Adds the given card infos to the queue otherwise adds None to all keys
    def add(self, card_info: dict[str, list[CardInfo]]):
        # shift all queues to the left
        for key in self.dict:
            if (len(self.dict[key]) >= self.buffer_size):
                self.dict[key].pop(0)
            # after popping (if queue full), add to queue
            if (key not in card_info):
                self.dict[key].append(None)
            else:
                if (len(card_info[key]) > 1):
                    print("ERROR: more than 1 card info in card_info dict. In CardInfoQueues.add()")
                elif (len(card_info[key]) == 1):
                    self.dict[key].append(card_info[key][0])

    def get(self, card_type: str) -> list[CardInfo]:
        return self.dict[card_type]

    # returns true if the card is moving
    def is_card_moving(self, card_type: str, thresh_card_moving) -> bool:
        avg_card_loc = self.get_avg_loc(card_type, thresh_card_moving)
        if (avg_card_loc is None):
            return True
        return False

    # returns the maximum x and y component difference in the queue for the given card type
    def get_max_loc_diff(self, card_type: str):
        # initialize to max int and 0
        x_max = 0
        x_min = sys.maxsize
        y_max = 0
        y_min = sys.maxsize
        num_cards = 0

        # find max and min x and y
        for card_info in self.dict[card_type]:
            if (card_info is not None):
                num_cards += 1
                loc = card_info.get_location()
                # x
                if (loc[0] > x_max):
                    x_max = loc[0]
                elif (loc[0] < x_min):
                    x_min = loc[0]
                # y
                if (loc[1] > y_max):
                    y_max = loc[1]
                elif (loc[1] < y_min):
                    y_min = loc[1]
        return (x_max - x_min, y_max - y_min) if (num_cards >= self.THRESH_NUM_CARD_INFOS) else None

    # Returns the average location of the card type if there are enough card infos in the queue
    # AND if the card is not moving. Otherwise returns None.
    def get_avg_loc(self, card_type: str, thresh_card_moving):
        sum_loc_x = 0
        sum_loc_y = 0
        num_cards = 0

        for card_info in self.dict[card_type]:
            if (card_info is not None):
                loc = card_info.get_location()
                # check if card is moving
                if (num_cards >= 1):
                    avg_loc_x = sum_loc_x / num_cards
                    avg_loc_y = sum_loc_y / num_cards
                    diff = abs(loc[0] - avg_loc_x) + abs(loc[1] - avg_loc_y)
                    if (diff > thresh_card_moving):
                        # card is moving, return None
                        return None
                num_cards += 1
                sum_loc_x += loc[0]
                sum_loc_y += loc[1]
        # return average location if there are enough card infos, otherwise return None
        if (num_cards >= self.THRESH_NUM_CARD_INFOS):
            return (int(sum_loc_x / num_cards), int(sum_loc_y / num_cards))
        return None

    # returns a dictionary of the average locations for non moving cards
    def get_avg_locs(self, thresh_card_moving):
        avg_locs = {}
        for card_type in self.dict:
            loc = self.get_avg_loc(card_type, thresh_card_moving)
            if (loc is not None):
                avg_locs[card_type] = loc
        return avg_locs

    # if the entire queue contain only None or length == 0, then the key is empty
    # also mark as empty if THRESH_NUM_CARD_INFOS or less card infos in queue
    def is_key_empty(self, card_type: str) -> bool:
        if (all(card_info is None for card_info in self.dict[card_type]) or (len(self.dict[card_type]) == 0)):
            return True
        card_info_count = 0
        for card_info in self.dict[card_type]:
            if (card_info is not None):
                card_info_count += 1
                if (card_info_count >= self.THRESH_NUM_CARD_INFOS):
                    return False
        return True

    # returns true if all keys are empty
    # AKA: all queues contain only None or empty or have less than THRESH_NUM_CARD_INFOS card infos
    def is_empty(self) -> bool:
        return all(self.is_key_empty(card_type) for card_type in self.dict)

    def __str__(self):
        return str(self.dict)

    def __repr__(self):
        return str(self.dict)


if __name__ == "__main__":
    engine = BlackJAIEngine()
    
    # Json data card layout:
    # Player: 7S and 8S close together on top left section
    # Player: AH and 3D close together on top right section
    # Dealer: 8C on bottom middle section
    json_data = {
        "predictions": [
            {
                "x": 282,
                "y": 301.5,
                "width": 44,
                "height": 41,
                "confidence": 0.944,
                "class": "7S"
            },
            {
                "x": 526.5,
                "y": 228,
                "width": 47,
                "height": 28,
                "confidence": 0.93,
                "class": "8S"
            },
            {
                "x": 485,
                "y": 304,
                "width": 44,
                "height": 40,
                "confidence": 0.926,
                "class": "7S"
            },
            {
                "x": 1100,
                "y": 290.5,
                "width": 44,
                "height": 29,
                "confidence": 0.924,
                "class": "AH"
            },
            {
                "x": 1200,
                "y": 320,
                "width": 44,
                "height": 29,
                "confidence": 0.924,
                "class": "3D"
            },
            {
                "x": 600,
                "y": 600,
                "width": 44,
                "height": 29,
                "confidence": 0.924,
                "class": "8C"
            }
        ]
    }

    engine.update(json_data)
    
    # feed the same json data to fill the buffer
    for i in range(30):
        engine.update(json_data)

    print(engine.frame_card_info_queues)
