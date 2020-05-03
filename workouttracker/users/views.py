from .models import Workouts, Action
from django.contrib import messages
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import UserPassesTestMixin
from django.shortcuts import render, redirect, get_object_or_404
from .forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, RedirectView

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

@login_required
def profile_update(request):
  if request.method == 'POST':
    u_form = UserUpdateForm(request.POST, instance=request.user)
    p_form = ProfileUpdateForm(request.POST, instance=request.user.profile)
    if u_form.is_valid() and p_form.is_valid():
      u_form.save()
      p_form.save()
      messages.success(request, f'Profile Updated!')
      return redirect('profile')
  else:
    u_form = UserUpdateForm(instance=request.user)
    p_form = ProfileUpdateForm(instance=request.user.profile)
  context = {
    'u_form': u_form,
    'p_form': p_form
  }
  return render(request, 'users/profileupdate.html', context)

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

  def form_valid(self, form):
    form.instance.author = self.request.user
    return super().form_valid(form)

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

class WorkoutDeleteView(UserPassesTestMixin, DeleteView):
  model = Workouts
  success_url = '/feed/'
  template_name = 'users/workoutdelete.html'

  def test_func(self):
    workout = self.get_object()
    if self.request.user == workout.author:
      return True
    else:
      return False

class LikeRedirectView(RedirectView):
  model = Workouts
  is_permanent = True
  def get_redirect_url(self, *args, **kwargs):
    pk = self.kwargs['pk']
    print(Workouts.objects.get(pk=pk).author)
    print(self.request.user)
    print(self.request.user == Workouts.objects.get(pk=pk).author)
    if self.request.user != Workouts.objects.get(pk=pk).author:
      try:
        action = Action.objects.get(user_liking=self.request.user, post_liked=Workouts.objects.get(pk=pk))
      except:
        new_like = Action(user_liking=self.request.user, post_liked=Workouts.objects.get(pk=pk), liked=True, disliked=False)
        workout = Workouts.objects.get(pk=pk)
        workout.likes = workout.likes + 1
        new_like.save()
        workout.save()
      else:
        if action.liked == False:
          action.disliked = False
          action.liked = True
          workout = Workouts.objects.get(pk=pk)
          workout.likes = workout.likes + 1
          workout.dislikes = workout.dislikes - 1
          action.save()
          workout.save()
    url = f'/workout/{pk}/'
    return url

  # def test_func(self):
  #   workout = self.get_object()
  #   if self.request.user != workout.author:
  #     return True
  #   else:
  #     return False

class DislikeRedirectView(RedirectView):
  model = Workouts
  is_permanent = True
  def get_redirect_url(self, *args, **kwargs):
    pk = self.kwargs['pk']
    print(Workouts.objects.get(pk=pk).author)
    print(self.request.user)
    print(self.request.user == Workouts.objects.get(pk=pk).author)
    if self.request.user != Workouts.objects.get(pk=pk).author:
      try:
        action = Action.objects.get(user_liking=self.request.user, post_liked=Workouts.objects.get(pk=pk))
      except:
        new_like = Action(user_liking=self.request.user, post_liked=Workouts.objects.get(pk=pk), liked=False, disliked=True)
        workout = Workouts.objects.get(pk=pk)
        workout.dislikes = workout.dislikes + 1
        new_like.save()
        workout.save()
      else:
        if action.disliked == False:
          action.disliked = True
          action.liked = False
          workout = Workouts.objects.get(pk=pk)
          workout.likes = workout.likes - 1
          workout.dislikes = workout.dislikes + 1
          action.save()
          workout.save()
    url = f'/workout/{pk}/'
    return url