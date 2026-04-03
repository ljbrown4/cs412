# File: models.py
# Author: Leigh Brown (ljbrown@bu.edu), 4/02/2026
# Description: create models and their attributes (joke, picture)
from django.db import models
from django.urls import reverse

# Create your models here.

class Joke(models.Model):
    '''class that creates a database to store jokes, their contributor, and a timestamp'''

    joke = models.TextField()
    contributor = models.TextField()
    timestamp = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.contributor} contributed {self.joke} at {self.timestamp}'
    
class Picture(models.Model):
    '''class that creates a database to store silly pictures, their contributor, and a timestamp'''

    image_url = models.URLField(blank=True)
    contributor = models.TextField()
    timestamp = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.contributor} contributed {self.image_url} at {self.timestamp}'
