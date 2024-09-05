import logging
from ninja import NinjaAPI, Form
from .models import Card, CardRating, Deck
from .schemas import CardSchema, CardRatingSchema, RatingsUploadSchema, DeckInputSchema,DeckSchema, Error
from .get_cards_from_json import get_cards_from_json, get_all_cards_from_json

api = NinjaAPI(title='Altered-TCG API', version='0.1')


@api.get('/get_card/{id}', response={200: CardSchema, 404: Error}, tags=["Card"])
def get_card(request, id: str):
    card = Card.objects.filter(id=id).first()
    if card is None:
        card_api = get_cards_from_json(id)
        if card_api is None:
            return 404, {'message': 'Card not found'}
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


@api.post('/upload_ratings', response={200: list[CardRatingSchema], 404: Error}, tags=["Card"])
def upload_ratings(request, card_ratings: list[RatingsUploadSchema]):
    rating_models = []
    for card_rating in card_ratings:
        for index, (hero_id, rating_value) in enumerate(card_rating.ratings.items()):
            card = Card.objects.get(id=card_rating.id)
            if card is None:
                break
            hero = Card.objects.get(id=hero_id)
            if hero is not None:
                new_rating = CardRating.objects.create(card_id=card, hero_id=hero, rating=rating_value)
                rating_models.append(new_rating)
    rating_models = CardRating.objects.bulk_create(objs=rating_models, ignore_conflicts=True)
    return 200, rating_models


@api.post("/upload_deck", response={200: DeckSchema, 404: Error}, tags=["Deck"])
def upload_deck(request, deck: Form[DeckInputSchema]):
    list_of_lines = deck.deck_list.split("<br>")
    cards = []
    for line in list_of_lines:
        try:
            split_line = line.strip().split(" ")
            card = {
                "qty": int(split_line[0]),
                "id": split_line[1],
            }
            cards.append(card)
        except Exception as e:
            logging.warning(e)

    new_deck = Deck.objects.create(name=deck.deck_name, hero=deck.hero_id, cards=cards)
    new_deck.set_deck_rating()
    new_deck.save()
    return 200, new_deck


def _init_kwargs(model, arg_dict):
    model_fields = [f.name for f in model._meta.get_fields()]
    return {k: v for k, v in arg_dict.items() if k in model_fields}