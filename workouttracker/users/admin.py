from django.contrib import admin
from .models import Workouts, Action, Comments, SavedPost, Profile

admin.site.register(Profile)
admin.site.register(Workouts)
admin.site.register(Action)
admin.site.register(Comments)
admin.site.register(SavedPost)