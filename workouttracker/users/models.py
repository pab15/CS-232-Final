from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.contrib.auth.models import User

class Profile(models.Model):
  user = models.OneToOneField(User, on_delete=models.CASCADE)
  bio = models.TextField(blank=True, null=True)
  
  def __str__(self):
    return f'{self.user.username} Profile'

class Workouts(models.Model):
  title = models.CharField(max_length=100)
  content = models.TextField()
  date_posted = models.DateTimeField(default=timezone.now)
  author = models.ForeignKey(User, on_delete=models.CASCADE)
  likes = models.IntegerField(default=0)
  dislikes = models.IntegerField(default=0)

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
  user_saving = models.ForeignKey(User, on_delete=models.CASCADE)
  post_saved = models.ForeignKey(Workouts, on_delete=models.CASCADE)

class Comments(models.Model):
  user_commenting = models.ForeignKey(User, on_delete=models.CASCADE)
  post_commented = models.ForeignKey(Workouts, on_delete=models.CASCADE)
  comment = models.TextField()
  date_posted = models.DateTimeField(default=timezone.now)

