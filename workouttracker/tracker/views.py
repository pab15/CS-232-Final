from django.shortcuts import render
from django.http import HttpResponse

def home(request):
  return render(request, 'tracker/home.html')

def about(request):
  context = {
    'title': 'About'
  }
  return render(request, 'tracker/about.html', context)

def register(request):
  return render(request, 'tracker/register.html')