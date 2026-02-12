# File: models.py
# Author: Leigh Brown (ljbrown@bu.edu), 2/12/2026
# Description: create models and their attributes

from django.db import models

# Create your models here.

class Profile(models.Model):
    ''' Class that encapsulates data for user profiles'''

    username = models.TextField(blank=True)
    display_name = models.TextField(blank=True)
    bio_text = models.TextField(blank=True)
    join_date = models.DateTimeField(auto_now=True)
    profile_image_url = models.URLField(blank=True)

    def __str__(self):
        return f'{self.username} joined on {self.join_date}'
