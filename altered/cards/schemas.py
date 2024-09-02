from ninja import Schema
from .models import Card
from ninja.orm import create_schema

class Error(Schema):
    message: str
