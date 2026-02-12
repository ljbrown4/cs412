from django.shortcuts import render
from django.views.generic import ListView, DetailView
from .models import Profile

# Create your views here.

class ProfileListView(ListView):
    ''' show all the profiles stored in the database'''
    model = Profile
    template_name = 'mini_insta/show_all_profiles.html'
    context_object_name = 'profiles'


class ProfileDetailView(DetailView):
    '''Show the information for one profle.'''
    model = Profile
    template_name = 'mini_insta/show_profile.html'
    context_object_name = 'profile'