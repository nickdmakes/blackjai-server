from state import BlackJAIState, SHUFFLE_PHASE, DEAL_PHASE, TURN_PHASE
from models import Card, CardInfo


class BlackJAIEngine:
    def __init__(self, buffer_size=20, threshold_same_card=250):
        self.state = BlackJAIState()
        self.buffer_size = buffer_size
        self.threshold_same_card = threshold_same_card
        self.frame_card_info_queues = CardInfoQueues(buffer_size)

    def update(self, json_data):
        self._update_card_info_queues(json_data)
        # TODO: update state based on card info queues
        if (self.state == SHUFFLE_PHASE):
            if (not self.frame_card_info_queues.is_empty()):
                self.state = DEAL_PHASE
        elif (self.state == DEAL_PHASE):
            # determine when 5 distinct cards are not moving anymore

            # put final cards in player's hands
            pass
        elif (self.state == TURN_PHASE):
            pass
        else:
            # nothing
            pass

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
        # average their coordinates and confidence to get 1 card per card type (key) in card_dict
        for key in card_dict:
            cards = card_dict[key]
            if (len(cards) > 1):
                # find cards that are close enough
                for i in range(len(cards)):
                    for j in range(i + 1, len(cards)):
                        if (cards[i].get_loc_diff(cards[j]) < self.threshold_same_card):
                            # average coordinates and confidence
                            cards[i] = cards[i].avg_card_infos(cards[j])
                            # remove the card that was averaged
                            cards.pop(j)
                            j -= 1
        self.frame_card_info_queues.add(card_dict)


# A dictionary class with keys as playing cards and values as a queue of CardInfo objects
class CardInfoQueues:
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

    def add(self, card_info: dict[str: CardInfo]):
        # shift all queues to the left
        for key in self.dict:
            if (len(self.dict[key]) >= self.buffer_size):
                self.dict[key].pop(0)
            # after popping (if queue full), add to queue
            if (key not in card_info):
                self.dict[key].append(None)
            else:
                self.dict[key].append(card_info[key])

    def get(self, card_type: str) -> list[CardInfo]:
        return self.dict[card_type]

    def is_card_moving(self, card_type: str, threshold_card_moving) -> bool:
        # if all locations are close enough, then the card is not moving
        return all(self.dict[card_type][i].get_loc_diff(self.dict[card_type][i + 1]) < threshold_card_moving for i in range(len(self.dict[card_type]) - 1))

    # returns the maximum location difference between all card infos in the queue
    def _get_max_loc_diff(self, card_type: str):
        # TODO
        loc_diff = self.dict[card_type][0].get_loc_diff(self.dict[card_type][1])
        for i in range(1, len(self.dict[card_type]) - 1):
            loc_diff = max(loc_diff, self.dict[card_type][i].get_loc_diff(self.dict[card_type][i + 1]))
        return loc_diff

    def is_key_empty(self, card_type: str) -> bool:
        # if the entire queue contain only None, then the key is empty
        return all(card_info is None for card_info in self.dict[card_type]) or len(self.dict[card_type]) == 0

    # returns true if all keys are empty (aka all queues contain only None or empty)
    def is_empty(self) -> bool:
        # if all keys are empty, then the dictionary is empty
        return all(self.is_key_empty(card_type) for card_type in self.dict)

    def __str__(self):
        return str(self.dict)

    def __repr__(self):
        return str(self.dict)


if __name__ == "__main__":
    engine = BlackJAIEngine()
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
                "x": 505,
                "y": 274.5,
                "width": 44,
                "height": 29,
                "confidence": 0.924,
                "class": "AH"
            }
        ]
    }

    engine.update(json_data)
    print(engine.frame_card_info_queues)
