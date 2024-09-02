import uuid
from django.db import models
from django_extensions.db.models import AutoSlugField

FACTIONS = {
    "Axion": "Axion",
    "Bravos": "Bravos",
    "Lyra": "Lyra",
    "Muna": "Muna",
    "Ordis": "Ordis",
    "Yzmir": "Yzmir"
}

RARITY = {
    'common': "common",
    "rare": "rare",
    "unique": "unique"
}


class Faction(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    slug = AutoSlugField(populate_from='name')
    name = models.CharField(max_length=255)


class Card(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    slug = AutoSlugField(populate_from=['name', 'faction', 'rarity', 'version'])
    name = models.CharField(max_length=255)
    rarity = models.CharField(max_length=255)
    version = models.CharField(max_length=255, default="base")
    faction = models.CharField(max_length=20, choices=FACTIONS, default="Axion")
    upload_date = models.DateField()
    img_url = models.CharField(max_length=255)


class Hero(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)
    faction = models.CharField(max_length=20, choices=FACTIONS, default="Axion")
    img_url = models.CharField(max_length=255)


class CardRating(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    card_id = models.ForeignKey(Card, on_delete=models.CASCADE)
    hero_id = models.ForeignKey(Hero, on_delete=models.CASCADE)
    rating = models.IntegerField()  # 1-5

    class Meta:
        unique_together = ("card_id", "hero_id")

class Set(models.Model):
    id = models.CharField(max_length=100, primary_key=True)
    name = models.CharField(max_length=255)
    cards = models.ManyToManyField(Card)

# class Channel(models.Model):
#     channel_id = models.CharField(max_length=255, primary_key=True, unique=True)
#     videos = models.ManyToManyField(Card)
#
#     def add_videos(self, videos):
#         # add all the videos in one call opposed to multiple database hits
#         video_models = [Card(**video) for video in videos]
#         video_models = self.videos.bulk_create(objs=video_models)
#         # add all the updates to the many-to-many table
#         self.videos.add(*video_models)
#         self.save()
