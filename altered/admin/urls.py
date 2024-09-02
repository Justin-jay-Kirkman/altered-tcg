
from django.contrib import admin
from django.urls import path

from cards import views
from cards.api import api

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', api.urls),
    path('', views.landing, name='landing'),
]
