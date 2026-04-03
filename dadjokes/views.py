from django.shortcuts import render
from .models import Joke, Picture
from django.views.generic import TemplateView, ListView, DetailView
import random

#api imports
from rest_framework import generics
from .serializers import *

# Create your views here.


class RandomView(TemplateView): #couldn't figure out how to use Detail view here
    '''view to help display one random image and one random joke'''

    template_name = 'dadjokes/random.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        jokes = Joke.objects.all()
        pictures = Picture.objects.all()

        context['joke'] = random.choice(jokes)
        context['picture'] = random.choice(pictures)

        return context
    
class AllJokesView(ListView):
    '''view to display all jokes from Joke model'''
    model = Joke
    template_name = 'dadjokes/alljokes.html'
    context_object_name = 'jokes'

class JokeDetailView(DetailView):
    '''view to display one joke from model'''
    model = Joke
    template_name = 'dadjokes/joke.html'
    context_object_name = 'joke'


class AllPicturesView(ListView):
    '''view to display all jokes from Joke model'''
    model = Picture
    template_name = 'dadjokes/allpictures.html'
    context_object_name = 'pictures'

class PictureDetailView(DetailView):
    '''view to display one picture from model'''
    model = Picture
    template_name = 'dadjokes/picture.html'
    context_object_name = 'picture'

#api views
class JokeListAPIView(generics.ListCreateAPIView):
  '''An API view to return a listing of Jokes and to create an Joke.'''
  queryset = Joke.objects.all()
  serializer_class = JokeSerializer
 
class JokeDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
  '''An API view to return a Joke.'''
  queryset = Joke.objects.all()
  serializer_class = JokeSerializer

class RandomJokeAPIView(generics.RetrieveAPIView):
    '''An API view to return one random Joke.'''
    queryset = Joke.objects.all()
    serializer_class = JokeSerializer

    def get_object(self):
        jokes = Joke.objects.all()
        return random.choice(jokes)

class PictureListAPIView(generics.ListCreateAPIView):
  '''An API view to return a listing of Jokes and to create an Joke.'''
  queryset = Picture.objects.all()
  serializer_class = PictureSerializer
 
class PictureDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
  '''An API view to return a Joke.'''
  queryset = Picture.objects.all()
  serializer_class = PictureSerializer

class RandomPictureAPIView(generics.RetrieveAPIView):
    '''An API view to return one random Picture.'''
    queryset = Picture.objects.all()
    serializer_class = PictureSerializer

    def get_object(self):
        pictures = Picture.objects.all()
        return random.choice(pictures)