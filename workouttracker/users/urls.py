from . import views
from django.urls import path
from django.contrib.auth.decorators import login_required
from .views import WorkoutListView, WorkoutDetailView, WorkoutCreateView, WorkoutUpdateView, WorkoutDeleteView, LikeRedirectView, DislikeRedirectView, MyPostListView, SaveRedirectView, MySavesListView, LikedListView

urlpatterns = [
    path('feed/', login_required(WorkoutListView.as_view()), name='users-feed'),
    path('myworkouts/', login_required(MyPostListView.as_view()), name='users-myposts'),
    path('mysaves/', login_required(MySavesListView.as_view()), name='users-mysaves'),
    path('mylikes/', login_required(LikedListView.as_view()), name='users-mylikes'),
    path('workout/new/', login_required(WorkoutCreateView.as_view()), name='workout-create'),
    path('workout/<pk>/', login_required(WorkoutDetailView.as_view()), name='workout-full'),
    path('workout/<pk>/like', login_required(LikeRedirectView.as_view()), name='workout-like'),
    path('workout/<pk>/dislike', login_required(DislikeRedirectView.as_view()), name='workout-dislike'),
    path('workout/<pk>/save', login_required(SaveRedirectView.as_view()), name='workout-save'),
    path('workout/<pk>/update/', login_required(WorkoutUpdateView.as_view()), name='workout-update'),
    path('workout/<pk>/delete/', login_required(WorkoutDeleteView.as_view()), name='workout-delete'),
]