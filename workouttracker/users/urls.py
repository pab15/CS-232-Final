from . import views
from django.urls import path
from django.contrib.auth.decorators import login_required
from .views import WorkoutListView, WorkoutDetailView, WorkoutCreateView, WorkoutUpdateView

urlpatterns = [
    path('feed/', login_required(WorkoutListView.as_view()), name='users-feed'),
    path('workout/new/', login_required(WorkoutCreateView.as_view()), name='workout-create'),
    path('workout/<pk>/', login_required(WorkoutDetailView.as_view()), name='workout-full'),
    path('workout/<pk>/update', login_required(WorkoutUpdateView.as_view()), name='workout-update'),
]