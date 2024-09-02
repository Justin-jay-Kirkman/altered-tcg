import json
from datetime import datetime
from types import SimpleNamespace

from ninja import NinjaAPI
from .models import Card
from .schemas import Error
from .sim_youtube_videos import get_simulated_videos_by_channel

api = NinjaAPI(title='Altered-TCG API', version='0.1')



# @api.get('/videos-by-channel/{channel_id}', response={200: list[VideoSchema], 404: Error}, tags=["Channel"])
# def get_most_recent_videos(request, channel_id: str):
#     channel = Channel.objects.filter(channel_id=channel_id).first()
#     result_limit = 5
#     if channel is None:
#         youtube_api = get_simulated_videos_by_channel(channel_id)
#         if youtube_api is None:
#             return 404, {'message': 'Channel not found'}
#         else:
#             channel = Channel.objects.update_or_create(channel_id=channel_id)[0]
#             channel.add_videos(youtube_api)
#             results = youtube_api[:result_limit]
#     else:
#         video_query_set = Card.objects.filter(channel=channel_id).order_by('-upload_date')[:result_limit]
#         results = video_query_set.values()
#     return 200, results
