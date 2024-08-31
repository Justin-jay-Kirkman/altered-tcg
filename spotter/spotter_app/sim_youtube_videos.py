import json
import os
from datetime import datetime


def get_simulated_videos_by_channel(channel_id):
    #windows
    json_file_path = os.path.join(os.path.dirname(__file__)) + "\\data\\videos.json"
    #linux
    #json_file_path = os.path.join(os.path.dirname(__file__)) + "/data/videos.json"
    with open(json_file_path, 'r') as file:
        data = json.loads(file.read())
    for channel in data:
        if channel == channel_id:
            return _fix_video_datatypes(data[channel])
    return None


def _fix_video_datatypes(youtube_api):
    for video in youtube_api:
        # need to convert upload_date from string to date for VideoSchema and models
        video["upload_date"] = datetime.strptime(video["upload_date"], "%Y-%m-%d").date()
    return youtube_api