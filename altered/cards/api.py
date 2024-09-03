import json
from datetime import datetime
from types import SimpleNamespace

from ninja import NinjaAPI
from .models import Card
from .schemas import CardSchema, Error
from .get_cards_from_json import get_cards_from_json, get_all_cards_from_json

api = NinjaAPI(title='Altered-TCG API', version='0.1')


@api.get('/get_card/{id}', response={200: CardSchema, 404: Error}, tags=["Card"])
def get_card(request, id: str):
    card = Card.objects.filter(id=id).first()
    if card is None:
        card_api = get_cards_from_json(id)
        if card_api is None:
            return 404, {'message': 'Channel not found'}
        else:
            kwargs = _init_kwargs(Card, card_api)
            card = Card.objects.create(**kwargs)
            card.save()
            results = card
    else:
        card_query_set = Card.objects.filter(id=id)
        results = card_query_set.values()
    return 200, results

# This can be created as a task in celery if needed in prod
@api.get('/bulk_card_upload', response={200: list[CardSchema], 404: Error}, tags=["Card"])
def bulk_card_upload(request):
    cards = get_all_cards_from_json()
    card_models = [Card(**_init_kwargs(Card, cards[card])) for card in cards]
    card_models = Card.objects.bulk_create(objs=card_models, ignore_conflicts=True)
    return 200, card_models


def _init_kwargs(model, arg_dict):
    model_fields = [f.name for f in model._meta.get_fields()]
    return {k: v for k, v in arg_dict.items() if k in model_fields}