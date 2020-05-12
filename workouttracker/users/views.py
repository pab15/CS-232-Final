from django.contrib import messages
from django.contrib.auth.models import User
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import UserPassesTestMixin
from .models import Workouts, Action, SavedPost, Comments, Profile
from django.shortcuts import render, redirect, get_object_or_404
from .forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm, CommentForm
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, RedirectView, FormView

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
  success_url = ''
  fields = ['comment']

  # def form_valid(self, form, **kwargs):
  #   pk = self.kwargs['pk']
  #   form.instance.user_commenting = self.request.user
  #   form.instance.post_commented = Workouts.objects.get(pk=pk)
  #   return super().form_valid(form)

  # def post(self, request, *args, **kwargs):
  #   pk = self.kwargs['pk']
  #   self.get_url()
  #   return FormView.post(self, request, user_commenting=self.request.user, post_commented=Workouts.objects.get(pk=pk))

  # def get_url(self, **kwargs):
  #   pk = self.kwargs['pk']
  #   self.success_url = f'/workout/{pk}/'

  # def get_context_data(self, **kwargs):
  #   pk = self.kwargs['pk']
  #   context = super(WorkoutDetailView, self).get_context_data(**kwargs)
  #   context['comments'] = Comments.objects.filter(post_commented=Workouts.objects.get(pk=pk))
  #   context['form'] = CommentForm
  #   return context

class CommentFormView(FormView):
  form_class = CommentForm
  success_url = ''

  def get_url(self, **kwargs):
    pk = self.kwargs['pk']
    self.success_url = f'/workout/{pk}/'

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
        if action.liked == True and action.disliked == False:
          action.disliked = False
          action.liked = False
          workout = Workouts.objects.get(pk=pk)
          workout.likes = workout.likes - 1
          action.save()
          workout.save()
        elif action.liked == False and action.disliked == True:
          action.disliked = False
          action.liked = True
          workout = Workouts.objects.get(pk=pk)
          workout.likes = workout.likes + 1
          workout.dislikes = workout.dislikes - 1
          action.save()
          workout.save()
        elif action.liked == False and action.disliked == False:
          action.disliked = False
          action.liked = True
          workout = Workouts.objects.get(pk=pk)
          workout.likes = workout.likes + 1
          action.save()
          workout.save()
    url = f'/workout/{pk}/'
    return url

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
        if action.disliked == True and action.liked == False:
          action.disliked = False
          action.liked = False
          workout = Workouts.objects.get(pk=pk)
          workout.dislikes = workout.dislikes - 1
          action.save()
          workout.save()
        elif action.disliked == False and action.liked == True:
          action.disliked = True
          action.liked = False
          workout = Workouts.objects.get(pk=pk)
          workout.likes = workout.likes - 1
          workout.dislikes = workout.dislikes + 1
          action.save()
          workout.save()
        elif action.disliked == False and action.liked == False:
          action.disliked = True
          action.liked = False
          workout = Workouts.objects.get(pk=pk)
          workout.dislikes = workout.dislikes + 1
          action.save()
          workout.save()
    url = f'/workout/{pk}/'
    return url

class SaveRedirectView(RedirectView):
  model = Workouts
  is_permanent = True
  def get_redirect_url(self, *args, **kwargs):
    pk = self.kwargs['pk']
    print(Workouts.objects.get(pk=pk).author)
    print(self.request.user)
    print(self.request.user == Workouts.objects.get(pk=pk).author)
    if self.request.user != Workouts.objects.get(pk=pk).author:
      try:
        print('entered try')
        saved_post = SavedPost.objects.get(user_saving=self.request.user, post_saved=Workouts.objects.get(pk=pk))
        saved_post.delete()
        url = f'/workout/{pk}/'
        return url
      except:
        print('entered except')
        new_save = SavedPost(user_saving=self.request.user, post_saved=Workouts.objects.get(pk=pk))
        new_save.save()
        url = f'/workout/{pk}/'
        return url

class MyPostListView(ListView):
  model = Workouts
  template_name = 'users/myposts.html'
  context_object_name = 'posts'
  ordering = ['-date_posted']

class MySavesListView(ListView):
  model = SavedPost
  template_name = 'users/savedposts.html'
  context_object_name = 'saved'

class LikedListView(ListView):
  model = Action
  template_name = 'users/mylikes.html'
  context_object_name = 'actions'

class UserDetailView(DetailView):
  model = User
  template_name = 'users/userview.html'
  
  def get_context_data(self, **kwargs):
    pk = self.kwargs['pk']
    context = super(UserDetailView, self).get_context_data(**kwargs)
    users = User.objects.all()
    for user in users:
      print(user.id)
      print(User.objects.get(username=User.objects.get(id=user.id)))
    context['user'] = User.objects.get(username=User.objects.get(id=pk))
    return context

class UserPostListView(ListView):
  model = Workouts
  template_name = 'users/userposts.html'
  ordering = ['-date_posted']

  def get_context_data(self, **kwargs):
    pk = self.kwargs['pk']
    context = super(UserPostListView, self).get_context_data(**kwargs)
    user_posted = User.objects.get(id=pk)
    context['posts'] = Workouts.objects.filter(author=user_posted)
    return context

class UserSaveListView(ListView):
  model = SavedPost
  template_name = 'users/usersavedposts.html'
  ordering = ['-date_posted']

  def get_context_data(self, **kwargs):
    pk = self.kwargs['pk']
    context = super(UserSaveListView, self).get_context_data(**kwargs)
    user_posted = User.objects.get(id=pk)
    context['saved'] = SavedPost.objects.filter(user_saving=user_posted)
    context['username'] = user_posted.username
    return context

class UserLikeListView(ListView):
  model = Action
  template_name = 'users/userlikedposts.html'
  ordering = ['-date_posted']

  def get_context_data(self, **kwargs):
    pk = self.kwargs['pk']
    context = super(UserLikeListView, self).get_context_data(**kwargs)
    user_liking = User.objects.get(id=pk)
    context['actions'] = Action.objects.filter(user_liking=user_liking)
    context['username'] = user_liking.username
    return context