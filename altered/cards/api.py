import logging
from ninja import NinjaAPI, Form
from .models import Card, CardRating, Deck
from .schemas import CardSchema, CardRatingSchema, RatingsUploadSchema, DeckInputSchema, DeckSchema, DeckOutputSchema, Error
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

@api.get("/suggest_deck/{hero_id}", response={200: DeckOutputSchema, 404: Error}, tags=["Deck"])
def suggest_deck(request, hero_id: str):
    deck = ""
    deck_rating = 0
    card = Card.objects.filter(id=hero_id).first()
    hero_name = card.name['en']
    cards = {
        card.id: {
            "qty": 1,
            "id": card.id,
            "name": hero_name
        }
    }
    if card is None:
        return 404, {'message': 'Hero not found'}
    else:
        ratings_query = CardRating.objects.filter(hero_id=card).order_by('-rating','card_id__rarity')
        ratings = list(ratings_query)

        cards_left = 39
        max_of_each_card = 3
        card_max = {}
        rares_left = 15
        for rating in ratings:
            card_name = rating.card_id.name['en']
            if cards_left == 0:
                break
            # Skip KS versions at this time
            if 'COREKS' in rating.card_id.id:
                continue
            # Skip Rares if total is already met
            if rares_left == 0 and rating.card_id.rarity == 'RARE':
                continue
            # Create default to add to
            if card_name not in card_max:
                card_max[card_name] = 0
            while cards_left > 0:
                if rares_left == 0 or card_max[card_name] == max_of_each_card:
                    break
                if rating.card_id.id not in cards:
                    cards[rating.card_id.id] = {
                        "qty": 0,
                        "id": rating.card_id.id,
                        "name": card_name,
                        "rarity": rating.card_id.rarity,
                        "rating": rating.rating
                    }
                cards[rating.card_id.id]["qty"] += 1
                card_max[card_name] += 1
                cards_left -= 1
                if rating.card_id.rarity == 'RARE':
                    rares_left -= 1
                deck_rating += rating.rating
        for card in cards:
            deck += "{Qty} {ID}<br>".format(Qty=cards[card]['qty'], ID=cards[card]['id'])

        return 200, {
            "hero": hero_name,
            "deck": deck,
            "deck_rating": deck_rating,
            "normalized_rating": int((deck_rating - 39) / (195-39)*100)
        }


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