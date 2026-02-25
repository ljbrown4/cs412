# File: forms.py
# Author: Leigh Brown (ljbrown@bu.edu), 2/19/2026 + 2/25/2026
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