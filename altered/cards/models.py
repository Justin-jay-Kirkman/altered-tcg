import uuid
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
    rating = models.IntegerField()  # 1-5
    updated_at = models.DateTimeField(auto_now=True)
    slug = AutoSlugField(populate_from=['card_id', 'hero_id'])

    def __str__(self):
        return self.card_id.name['en'] + " | " + self.hero_id.name['en'] + " | " + str(self.rating)

