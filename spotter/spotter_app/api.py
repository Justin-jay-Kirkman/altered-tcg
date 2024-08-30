from ninja import NinjaAPI
from .models import Channel, Video
from .schemas import VideoSchema, Error
from django.shortcuts import get_object_or_404

api = NinjaAPI(title='Spotter API', version='0.1')


@api.get('/videos-by-channel/{channel_id}', response={200: VideoSchema, 404: Error}, tags=["Channel"])
def get_most_recent_videos(request, channel_id: str):
    channel = get_object_or_404(Channel, id=channel_id)
    return channel