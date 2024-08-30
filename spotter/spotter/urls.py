
from django.contrib import admin
from django.urls import path

from spotter_app import views
from spotter_app.api import api

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', api.urls),
    path('', views.landing, name='landing'),
]
