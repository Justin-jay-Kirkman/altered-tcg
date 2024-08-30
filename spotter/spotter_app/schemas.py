from ninja import Schema
from .models import Channel, Video
from ninja.orm import create_schema

ChannelSchema = create_schema(Channel, depth=1,name='Channel')
VideoSchema = create_schema(Video, name='Video')


class Error(Schema):
    message: str
