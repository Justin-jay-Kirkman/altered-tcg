import uuid

from django.conf import settings
from django.contrib.auth.models import User
from django.db import models
from django_extensions.db.models import AutoSlugField
from .enums import TYPES, SUB_TYPES, FACTIONS, RARITY
from .defaults import get_default_name, get_default_image_path


class Card(models.Model):
    id = models.CharField(max_length=100, primary_key=True)
    type = models.CharField(max_length=100, choices=TYPES, default=next(iter(TYPES)))
    subType = models.JSONField(default=list, choices=SUB_TYPES)
    name = models.JSONField(default=get_default_name)
    rarity = models.CharField(max_length=20, choices=RARITY, default=next(iter(RARITY)))
    version = models.CharField(max_length=255, default="base")
    mainFaction = models.CharField(max_length=20, choices=FACTIONS, default=next(iter(FACTIONS)))
    imagePath = models.JSONField(default=get_default_image_path)
    imageThumbnail = models.CharField(max_length=255, default="") # Use this when linking two
    elements = models.JSONField(default=dict)

    def __str__(self):
        return self.name["en"] + " | " + self.mainFaction + " | " + self.rarity + " | " + self.version


class CardRating(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    card_id = models.ForeignKey(Card, on_delete=models.CASCADE, related_name="card")
    hero_id = models.ForeignKey(Card, on_delete=models.CASCADE, related_name="hero")
    rating = models.IntegerField(default=1)  # 1-5
    updated_at = models.DateTimeField(auto_now=True)
    version = models.IntegerField(default=1)
    slug = AutoSlugField(populate_from=['card_id', 'hero_id'])

    def __str__(self):
        return self.card_id.name['en'] + " | " + self.hero_id.name['en'] + " | " + str(self.rating)

class Deck(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="decks", null=True)
    name = models.CharField(max_length=255)
    hero = models.CharField(max_length=255)
    cards = models.JSONField(default=list)
    rating = models.IntegerField(default=1)
    ratings = models.JSONField(default=list)
    updated_at = models.DateTimeField(auto_now=True)
    slug = AutoSlugField(populate_from=['name'])

    def normalized_rating(self):
        return int((self.rating - 39) / (390-39)*100)

    def set_deck_rating(self):
        hero = Card.objects.get(id=self.hero)
        self.rating = 0
        self.ratings = []
        for card_json in self.cards:
            try:
                card = Card.objects.get(id=card_json["id"])
            except Card.DoesNotExist:
                self.rating += 10
                self.ratings.append({
                    "id": card_json["id"],
                    "qty": card_json["qty"],
                    "name": "Unique",
                    "rating": 5
                })
                continue
            if card.type != "HERO":
                Qty = card_json.get("qty")
                card_ratings = CardRating.objects.filter(card_id=card, hero_id=hero).order_by("-updated_at").first()
                self.rating += (Qty * card_ratings.rating)
                self.ratings.append({
                    "id": card.id,
                    "qty": card_json["qty"],
                    "name": card.name["en"],
                    "rarity": card.rarity,
                    "rating": card_ratings.rating
                })
            else:
                # if hero added in upload, overwrite deck hero
                hero = card
                self.hero = card.id

    def __str__(self):
        return self.name + " | " + str(self.normalized_rating())


# Skip uniques for now
class Collection(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255, default="test")
    # user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="collections")
    cards = models.JSONField(default=dict)
