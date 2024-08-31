from django.db import models


class Video(models.Model):
    video_id = models.CharField(max_length=100, primary_key=True)
    video_title = models.CharField(max_length=255)
    upload_date = models.DateField()


class Channel(models.Model):
    channel_id = models.CharField(max_length=255, primary_key=True, unique=True)
    videos = models.ManyToManyField(Video)

    def add_videos(self, videos):
        # add all the videos in one call opposed to multiple database hits
        video_models = [Video(**video) for video in videos]
        video_models = self.videos.bulk_create(objs=video_models)
        # add all the updates to the many-to-many table
        self.videos.add(*video_models)
        self.save()
