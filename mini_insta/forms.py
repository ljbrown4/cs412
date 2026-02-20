# File: forms.py
# Author: Leigh Brown (ljbrown@bu.edu), 2/19/2026
# Description: create forms and their fields (post)

from django import forms
from .models import *

class CreatePostForm(forms.ModelForm):
    '''A form to add an article to the database'''

    class Meta:
        '''assoc this form with a model from our database'''
        model = Post
        fields = ['caption']