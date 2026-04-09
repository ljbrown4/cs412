# File: forms.py
# Author: Leigh Brown (ljbrown4@bu.edu), 2/19/2026 + 2/25/2026
# Description: create forms and their fields (post)

from django import forms
from .models import *

class CreatePostForm(forms.ModelForm):
    '''A form to add a post to the database'''

    class Meta:
        '''assoc this form with post model from our database'''
        model = Post
        fields = ['caption']

class UpdateProfileForm(forms.ModelForm):
    '''form to update fields in an already created profile'''

    class Meta:
        '''assoc this form with profile model from database'''
        model = Profile
        fields = ['display_name', 'bio_text', 'profile_image_url']

class UpdatePostForm(forms.ModelForm):
    '''form to update fields in an already created post'''

    class Meta:
        '''assoc this form with post model from database'''
        model = Post
        fields = ['caption']


class CreateProfileForm(forms.ModelForm):
    '''form to handle profile creation'''

    class Meta:
        '''assoc this form with profile model from database'''
        model = Profile
        fields = ['username','display_name', 'bio_text','profile_image_url']


class CreateCommentForm(forms.ModelForm):
    '''form to add comment on a post'''

    class Meta:
        model = Comment
        fields = ['text']
