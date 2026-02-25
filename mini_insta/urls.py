# File: urls.py
# Author: Leigh Brown (ljbrown@bu.edu), 2/12/2026 + 2/19/2026
# Description: paths to each page

from django.urls import path
from django.conf import settings
from . import views
from .views import *
 
 
urlpatterns = [
    path('', ProfileListView.as_view(), name="show_all_profiles"),
    path('profile/<int:pk>', ProfileDetailView.as_view(), name='profile'),
    path('post/<int:pk>', PostDetailView.as_view(), name='post'),
    path('profile/<int:pk>/post/create', CreatePostView.as_view(), name="create_post"), #assignment 4
    path('profile/<int:pk>/update', UpdateProfileView.as_view(), name="update_profile"), #assignment 5
    path('post/<int:pk>/delete', DeletePostView.as_view(), name="delete_post"), #assignment 5
    path('post/<int:pk>/update', UpdatePostView.as_view(), name="update_post"), #assignment 5
] 