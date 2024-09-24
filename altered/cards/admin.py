from django.contrib import admin
from .models import Card, CardRating, Deck, Collection

# Register your models here.
admin.site.register(Card)
admin.site.register(CardRating)
admin.site.register(Deck)
admin.site.register(Collection)