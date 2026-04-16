# File: urls.py
# Author: Leigh Brown (ljbrown4@bu.edu), 4/15/2026
# Description: paths to each page

from django.urls import path
from django.conf import settings
from . import views
from .views import *
from django.contrib.auth import views as auth_views

urlpatterns = [
    #adventure urls
    path('', AdventureListView.as_view(), name="home"),
    path('home', AdventureListView.as_view(), name="home"),
    path('adventure/<int:pk>', AdventureDetailView.as_view(), name="adventure"),
    path('create_adventure', CreateAdventureView.as_view(), name='create_adventure'),
    path('adventure/<int:pk>/update', UpdateAdventureView.as_view(), name='update_adventure'),
    path('adventure/<int:pk>/delete', DeleteAdventureView.as_view(), name='delete_adventure'),

    #destination urls
    path('adventure/<int:pk>/destinations', DestinationListView.as_view(), name="destinations"),
    path('destination/<int:pk>', DestinationDetailView.as_view(), name="destination"),
    path('adventure/<int:pk>/create_destination', CreateDestinationView.as_view(), name='create_destination'),
    path('destination/<int:pk>/update', UpdateDestinationView.as_view(), name='update_destination'),
    path('destination/<int:pk>/delete', DeleteDestinationView.as_view(), name='delete_destination'),

    #journal urls
    path('destination/<int:pk>/journals', JournalListView.as_view(), name="journals"),
    path('journal/<int:pk>', JournalDetailView.as_view(), name="journal"),
    path('destination/<int:pk>/create_journal', CreateJournalView.as_view(), name='create_journal'),
    path('journal/<int:pk>/update', UpdateJournalView.as_view(), name='update_journal'),
    path('journal/<int:pk>/delete', DeleteJournalView.as_view(), name='delete_journal'),

    #transportation urls
    path('destination/<int:pk>/transportations', TransportationListView.as_view(), name="transportations"),
    path('transportation/<int:pk>', TransportationDetailView.as_view(), name="transportation"),
    path('destination/<int:pk>/create_transportation', CreateTransportationView.as_view(), name='create_transportation'),
    path('transportation/<int:pk>/update', UpdateTransportationView.as_view(), name='update_transportation'),
    path('transportation/<int:pk>/delete', DeleteTransportationView.as_view(), name='delete_transportation'),

    #lodging urls
    path('destination/<int:pk>/lodgings', LodgingListView.as_view(), name="lodgings"),
    path('lodging/<int:pk>', LodgingDetailView.as_view(), name="lodging"),
    path('destination/<int:pk>/create_lodging', CreateLodgingView.as_view(), name='create_lodging'),
    path('lodging/<int:pk>/update', UpdateLodgingView.as_view(), name='update_lodging'),
    path('lodging/<int:pk>/delete', DeleteLodgingView.as_view(), name='delete_lodging'),

    #activity urls
    path('destination/<int:pk>/activities', ActivityListView.as_view(), name="activities"),
    path('activity/<int:pk>', ActivityDetailView.as_view(), name="activity"),
    path('destination/<int:pk>/create_activity', CreateActivityView.as_view(), name='create_activity'),
    path('activity/<int:pk>/update', UpdateActivityView.as_view(), name='update_activity'),
    path('activity/<int:pk>/delete', DeleteActivityView.as_view(), name='delete_activity'),

    #profile views
    path('profile/', ProfileDetailView.as_view(), name='profile'),
    path('create_profile/', CreateProfileView.as_view(), name='create_profile'),
    path('profile/update', UpdateProfileView.as_view(), name='update_profile'),

    #authentication
    path('login/', auth_views.LoginView.as_view(template_name="project/login.html"), name="login"), #assignment 6
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'), #assignment 6
]