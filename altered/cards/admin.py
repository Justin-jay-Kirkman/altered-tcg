from django.contrib import admin
from .models import Faction, Card, Hero, CardRating

# Register your models here.
admin.site.register(Faction)
admin.site.register(Card)
admin.site.register(Hero)
admin.site.register(CardRating)
