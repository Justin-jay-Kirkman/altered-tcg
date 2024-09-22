import uuid

from ninja import Schema
from .models import Card, CardRating, Deck
from ninja.orm import create_schema
from pydantic import ConfigDict


CardSchema = create_schema(Card, depth=2, name='Card')
CardRatingSchema = create_schema(CardRating, name='Card')
DeckSchema = create_schema(Deck, fields=['name', 'hero', 'rating'], name='Deck')


class RatingsUploadSchema(Schema):
    id: str
    faction: str
    ratings: dict = {
        "string": 0
    }


class DeckInputSchema(Schema):
    deck_name: str = ""
    hero_id: str = ""
    deck_list: str = ""

    model_config = ConfigDict(strict=False)


class DeckOutputSchema(Schema):
    hero: str = ""
    deck: str = "",
    deck_rating: int = 0,
    normalized_rating: int = 0

class Error(Schema):
    message: str

class Success(Schema):
    message: str