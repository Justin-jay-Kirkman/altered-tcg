from django.contrib import admin
from .models import Card, CardRating, Deck

# Register your models here.
admin.site.register(Card)
admin.site.register(CardRating)
admin.site.register(Deck)