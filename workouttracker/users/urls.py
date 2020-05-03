from . import views
from django.urls import path
from django.contrib.auth.decorators import login_required
from .views import WorkoutListView, WorkoutDetailView, WorkoutCreateView, WorkoutUpdateView, WorkoutDeleteView, LikeRedirectView, DislikeRedirectView

urlpatterns = [
    path('feed/', login_required(WorkoutListView.as_view()), name='users-feed'),
    path('workout/new/', login_required(WorkoutCreateView.as_view()), name='workout-create'),
    path('workout/<pk>/', login_required(WorkoutDetailView.as_view()), name='workout-full'),
    path('workout/<pk>/like', login_required(LikeRedirectView.as_view()), name='workout-like'),
    path('workout/<pk>/dislike', login_required(DislikeRedirectView.as_view()), name='workout-dislike'),
    path('workout/<pk>/update/', login_required(WorkoutUpdateView.as_view()), name='workout-update'),
    path('workout/<pk>/delete/', login_required(WorkoutDeleteView.as_view()), name='workout-delete'),
]