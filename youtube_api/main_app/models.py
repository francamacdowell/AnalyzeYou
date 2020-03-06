from django.db import models


class ChannelDetails(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=200)
    subs = models.IntegerField()
    views = models.IntegerField()
    profile_image_link = models.CharField(max_length=200)


class VideoDetails(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=200)
    description = models.TextField()
    tags = models.TextField()


class StatisticsDetails(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    sentiment_result = models.TextField()
    time_series = models.TextField()
    word_cloud = models.TextField()


class Setup(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    link_video = models.TextField()
    user_token = models.TextField()
