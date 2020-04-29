from . import views
from django.urls import path

urlpatterns = [
    path('', views.home, name='tracker-home'),
    path('about/', views.about, name='tracker-about'),
    path('signin/', views.signin, name='tracker-signin'),
    path('feed/', views.feed, name='tracker-feed')
]