from .models import Workouts
from django.shortcuts import render
from django.http import HttpResponse

def home(request):
  return render(request, 'tracker/home.html')

def about(request):
  context = {
    'title': 'About'
  }
  return render(request, 'tracker/about.html', context)

def signin(request):
  return render(request, 'tracker/signin.html')

def register(request):
  return render(request, 'tracker/register.html')

def feed(request):
  context = {
    'posts': Workouts.objects.all(),
    'content': []
  }
  return render(request, 'tracker/feed.html', context)