from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.contrib.auth.models import User

class Workouts(models.Model):
  title = models.CharField(max_length=100)
  content = models.TextField()
  date_posted = models.DateTimeField(default=timezone.now)
  author = models.ForeignKey(User, on_delete=models.CASCADE)

  def __str__(self):
    return self.title

  def get_absolute_url(self):
    return reverse('users-feed')

class Action(models.Model):
  user_liking = models.ForeignKey(User, on_delete=models.CASCADE)
  post_liked = models.ForeignKey(Workouts, on_delete=models.CASCADE)
  liked = models.BooleanField()
  disliked = models.BooleanField()

class SavedPost(models.Model):
  user = models.ForeignKey(User, on_delete=models.CASCADE)
  post_saved = models.ForeignKey(Workouts, on_delete=models.CASCADE)

class Comments(models.Model):
  user_commenting = models.ForeignKey(User, on_delete=models.CASCADE)
  post_commented = models.ForeignKey(Workouts, on_delete=models.CASCADE)
  comment = models.TextField()
  date_posted = models.DateTimeField(default=timezone.now)

