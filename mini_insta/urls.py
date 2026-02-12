# File: urls.py
# Author: Leigh Brown (ljbrown@bu.edu), 2/12/2026
# Description: paths to each page

from django.urls import path
from django.conf import settings
from . import views
from .views import ProfileListView, ProfileDetailView
 
 
urlpatterns = [
    path('', ProfileListView.as_view(), name="show_all_profiles"),
    path('profile/<int:pk>', ProfileDetailView.as_view(), name='profile')
] 