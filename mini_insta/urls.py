# File: urls.py
# Author: Leigh Brown (ljbrown@bu.edu), 2/12/2026 + 2/19/2026
# Description: paths to each page

from django.urls import path
from django.conf import settings
from . import views
from .views import *
from django.contrib.auth import views as auth_views
 
 
urlpatterns = [
    path('', ProfileListView.as_view(), name="show_all_profiles"),
    path('profile/<int:pk>', ProfileDetailView.as_view(), name='profile'),
    path('profile/', MyProfileDetailView.as_view(), name='my_profile'),
    path('post/<int:pk>', PostDetailView.as_view(), name='post'),

    # path('profile/<int:pk>/post/create', CreatePostView.as_view(), name="create_post"), #assignment 4
    path('profile/create_post', CreatePostView.as_view(), name="create_post"), #assignment 6

    # path('profile/<int:pk>/update', UpdateProfileView.as_view(), name="update_profile"), #assignment 5
    path('profile/update', UpdateProfileView.as_view(), name="update_profile"), #assignment 6

    # path('profile/<int:pk>/feed', PostFeedListView.as_view(), name="show_feed"), #assignment 5
    path('profile/feed', PostFeedListView.as_view(), name="show_feed"), #assignment 6

    path('post/<int:pk>/delete', DeletePostView.as_view(), name="delete_post"), #assignment 5
    path('post/<int:pk>/update', UpdatePostView.as_view(), name="update_post"), #assignment 5

    path('profile/<int:pk>/followers', ShowFollowersDetailView.as_view(), name="followers"), #assignment 5
    path('profile/<int:pk>/following', ShowFollowingDetailView.as_view(), name="following"), #assignment 5 

    # path('profile/<int:pk>/search', SearchView.as_view(), name='search'), #assignment 5
    path('profile/search', SearchView.as_view(), name='search'), #assignment 6

    path('login/', auth_views.LoginView.as_view(template_name="mini_insta/login.html"), name="login"), #assignment 6
    path('logout/', auth_views.LogoutView.as_view(next_page='logout_confirmation'), name='logout'), #assignment 6
    path("confirmation/", LogOutComfirmationView.as_view(), name="logout_confirmation"), #assignment 6

    path('create_profile/', CreateProfileView.as_view(), name="create_profile"), #assignment 6

    path('profile/<int:pk>/follow', CreateFollowView.as_view(), name='follow'), #assignment 6
    path('profile/<int:pk>/delete_follow', DeleteFollowView.as_view(), name='delete_follow'), #assignment 6
    path('post/<int:pk>/like', CreateLikeView.as_view(), name='like'), #assignment 6
    path('post/<int:pk>/delete_like', DeleteLikeView.as_view(), name='delete_like'), #assignment 6

    path('post/<int:pk>/comment', CreateCommentView.as_view(), name='create_comment'), #assignment 6 challenge
    path('comment/<int:pk>/delete', DeleteCommentView.as_view(), name='delete_comment'), #assignment 6 challenge


    #api views
    path('api/', PostFeedAPIView.as_view(), name="api_feed"),
    path('api/explore', ProfileListAPIView.as_view(), name="api_explore"),
    path('api/profile/<int:pk>', ProfileDetailAPIView.as_view(), name="api_profile"),
    path('api/post/<int:pk>', PostDetailAPIView.as_view(), name="api_post"),
    path('api/followers', FollowerListAPIView.as_view(), name="api_followers"),
    path('api/following', FollowingListAPIView.as_view(), name="api_following"),
    path('api/comments', CommentListAPIView.as_view(), name="api_comments"),
    path('api/comment/<int:pk>', CommentDetailAPIView.as_view(), name="api_comment"),
    path('api/likes', LikeListAPIView.as_view(), name="api_likes"),
    path('api/like/<int:pk>', LikeDetailAPIView.as_view(), name="api_like33"),
] 