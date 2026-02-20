# File: models.py
# Author: Leigh Brown (ljbrown@bu.edu), 2/12/2026
# Description: create models and their attributes (profile, post, photo)

from django.db import models
from django.urls import reverse
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
    
    def get_all_posts(self):
        '''get all posts by a user'''
        posts = Post.objects.filter(profile=self)
        return posts
    
    

class Post(models.Model):
    '''class that encapsulates data for a user's post '''

    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now=True)
    caption = models.TextField(blank=True)

    def __str__(self):
        '''return string rep of this comment'''
        return f'{self.profile} posted at {self.timestamp}'
    
    def get_all_photos(self):
        '''get all photos for a post'''
        photos = Photo.objects.filter(post=self)
        return photos

    def get_first_photo(self):
        '''get 1st photo for a post'''
        photos = Photo.objects.filter(post=self).first() #googled this
        return photos
    
    def get_absolute_url(self):
        '''return a url to display one instance of this mdel
        used to deal with config error when adding articles using form'''
        return reverse('post', kwargs={'pk':self.pk})

class Photo(models.Model):
    '''class that encapsulates data for a user's uploaded photos associated with a post '''

    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now=True)
    image_url = models.URLField(blank=True)

    def __str__(self):
        '''return string rep of this comment'''
        return f'image uploaded at {self.timestamp} associated with post: {self.post}'

