from django.db import models


class Video(models.Model):
    video_id = models.CharField(max_length=100, primary_key=True)
    video_title = models.CharField(max_length=255)
    upload_date = models.DateField()


class Channel(models.Model):
    channel_id = models.CharField(max_length=255, primary_key=True)
    channel_name = models.CharField(max_length=255)
    videos = models.ManyToManyField(Video)
