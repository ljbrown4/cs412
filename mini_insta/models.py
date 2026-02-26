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
        posts = Post.objects.filter(profile=self).order_by('-timestamp') #updated so newer posts are showcased first
        return posts
    
    def get_num_posts(self):
        '''get the # of posts a profile has'''
        get = self.get_all_posts()
        return len(get)
    
    def get_post_feed(self):
        '''returns all posts from users this profile follows'''

        # get following profiles
        following_set = Follow.objects.filter(follower_profile=self)

        # extract Profile 
        following_profiles = []
        for f in following_set:
            following_profiles.append(f.profile)

        # get posts from those profiles
        all_posts = Post.objects.filter(profile__in=following_profiles).order_by('-timestamp')

        return all_posts
    
    def get_followers(self):
        ''' get all followers of the curr profile'''
        followers_set = Follow.objects.filter(profile=self)
        followers = list(followers_set)
        return followers
    
    def get_num_followers(self):
        '''get the number of profiles that follow this profile'''
        get = self.get_followers()
        return len(get)
    
    def get_following(self):
        ''' get all profiles this profile follows'''
        following_set = Follow.objects.filter(follower_profile=self)
        following = list(following_set)
        return following
    
    def get_num_following(self):
        '''get the number of profiles that this profile follows'''
        get = self.get_following()
        return len(get)
    
    def get_absolute_url(self):
        '''return a url to display one instance of this mdel
        used to deal with config error when updating profile using a form'''
        return reverse('profile', kwargs={'pk':self.pk})
    
    

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
    
    def get_all_comments(self):
        '''get all comments on a post'''
        comments = Comment.objects.filter(post=self)
        return comments
    
    def get_likes(self):
        '''get all likes on a post'''
        likes = Like.objects.filter(post=self)
        return likes
    
    def get_first_like(self):
        '''get all likes on a post'''
        likes = Like.objects.filter(post=self).first()
        return likes
    
    def get_num_likes(self):
        '''get the number of profiles that follow this profile'''
        get = self.get_likes()
        return len(get) - 1 #bc first one is already displayed
    
    def get_absolute_url(self):
        '''return a url to display one instance of this mdel
        used to deal with config error when adding articles using form'''
        return reverse('post', kwargs={'pk':self.pk})

class Photo(models.Model):
    '''class that encapsulates data for a user's uploaded photos associated with a post '''

    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now=True)
    image_url = models.URLField(blank=True)
    image_file = models.ImageField(blank=True) #an actual image

    def get_image_url(self):
        if self.image_url:
            return self.image_url
        elif self.image_file:
            return self.image_file.url

    def __str__(self):
        '''return string rep of this comment'''
        return f'image uploaded at {self.timestamp} associated with post: {self.post}'
    

class Follow(models.Model):
    '''class that encapsulates data for profiles followed and that following'''
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name="profile")
    follower_profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name="follower_profile")
    timestamp = models.DateTimeField(auto_now=True)

    def __str__(self):
        '''return string rep of this comment'''
        return f'{self.follower_profile} followed {self.profile} at {self.timestamp}'
    
class Comment(models.Model):
    '''class that encapsulates data for comments on posts'''
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now=True)
    text = models.TextField(blank=False)

    def __str__(self):
        '''return string rep of this comment'''
        return f'{self.profile.username} commented {self.text}'
    

class Like(models.Model):
    ''' class that encapsulates data for likes on a post'''
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now=True)

    def __str__(self):
        '''return string rep of this comment'''
        return f'{self.profile} liked {self.post}'


