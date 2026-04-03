from django.urls import path
from django.conf import settings
from . import views
from .views import *

urlpatterns = [
    path('', RandomView.as_view(), name='home'),
    path('random', RandomView.as_view(), name='random'),
    path('jokes', AllJokesView.as_view(), name="jokes"),
    path('joke/<int:pk>', JokeDetailView.as_view(), name="joke"),
    path('pictures', AllPicturesView.as_view(), name="pictures"),
    path('picture/<int:pk>', PictureDetailView.as_view(), name="picture"),
    #api urls
    path('api/', RandomJokeAPIView.as_view(), name="api"),
    path('api/random', RandomJokeAPIView.as_view(), name="api_random"),
    path('api/jokes', JokeListAPIView.as_view(), name="api_jokes"),
    path('api/joke/<int:pk>', JokeDetailAPIView.as_view(), name="api_joke"),
    path('api/pictures', PictureListAPIView.as_view(), name="api_pictures"),
    path('api/picture/<int:pk>', PictureDetailAPIView.as_view(), name="api_picture"),
    path('api/random_picture', RandomPictureAPIView.as_view(), name="api_randpic"),
]