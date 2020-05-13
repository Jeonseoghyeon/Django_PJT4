from django.db import models
from django.conf import settings

# Create your models here.
class Movie(models.Model):
    title = models.CharField(max_length=100)
    poster = models.ImageField(blank=True)
    summary = models.TextField()

class Review(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    rank = models.IntegerField()
    movie = models.ForeignKey(Movie, on_delete='CASCADE', related_name='reviews')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete='CASCADE', related_name='write_reviews')
    like_users = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='like_reviews')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Comment(models.Model):
    content = models.CharField(max_length=140)
    review = models.ForeignKey(Review, on_delete='CASCADE', related_name='comments')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete='CASCADE', related_name='write_comments')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)