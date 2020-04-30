from .forms import UserRegisterForm
from .models import Workouts
from django.contrib import messages
from django.shortcuts import render, redirect
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import UserPassesTestMixin
from django.views.generic import ListView, DetailView, CreateView, UpdateView

def register(request):
  if request.method == 'POST':
    form = UserRegisterForm(request.POST)
    if form.is_valid():
      form.save()
      username = form.cleaned_data.get('username')
      messages.success(request, f'Account Created for {username}')
      return redirect('signin')
  else:
    form = UserRegisterForm()
  return render(request, 'users/register.html', {'form': form})

@login_required
def profile(request):
  return render(request, 'users/profile.html')

class WorkoutListView(ListView):
  model = Workouts
  template_name = 'users/feed.html'
  context_object_name = 'posts'
  ordering = ['-date_posted']

class WorkoutDetailView(DetailView):
  model = Workouts
  template_name = 'users/fullworkout.html'

class WorkoutCreateView(CreateView):
  model = Workouts
  template_name = 'users/createworkout.html'
  fields = ['title', 'content']

class WorkoutUpdateView(UserPassesTestMixin, UpdateView):
  model = Workouts
  template_name = 'users/updateworkout.html'
  fields = ['title', 'content']

  def form_valid(self, form):
    form.instance.author = self.request.user
    return super().form_valid(form)

  def test_func(self):
    workout = self.get_object()
    if self.request.user == workout.author:
      return True
    else:
      return False
