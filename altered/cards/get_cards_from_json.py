import json
import os


def get_cards_from_json(card_id):
    json_file_path = os.path.join(os.path.dirname(__file__)) + "/data/cards.json"
    with open(json_file_path, 'r', encoding="utf8") as file:
        data = json.loads(file.read())
    for card in data:
        if card == card_id:
            return data[card]
    return None


def get_all_cards_from_json():
    json_file_path = os.path.join(os.path.dirname(__file__)) + "/data/cards.json"
    with open(json_file_path, 'r', encoding="utf8") as file:
        data = json.loads(file.read())
    return data