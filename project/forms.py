# File: forms.py
# Author: Leigh Brown (ljbrown4@bu.edu), 4/15/2026
# Description: create forms and their fields 

from django import forms
from .models import *

#adventure forms
class CreateAdventureForm(forms.ModelForm):
    '''a form to add an adventure to the database'''

    class Meta:
        '''assoc thsi form with adventure model from the database'''
        model = Adventure
        fields = ['title', 'start_date', 'end_date', 'budget', 'cover_image']

class UpdateAdventureForm(forms.ModelForm):
    '''a form to add an adventure to the database'''

    class Meta:
        '''assoc thsi form with adventure model from the database'''
        model = Adventure
        fields = ['title', 'start_date', 'end_date', 'budget', 'cover_image', 'isCompleted']


#profile forms
class UpdateProfileForm(forms.ModelForm):
    '''form to update fields in an already created profile'''

    class Meta:
        '''assoc this form with profile model from database'''
        model = Profile
        fields = ['display_name', 'cover_image', 'profile_image', 'bio_text']

class CreateProfileForm(forms.ModelForm):
    '''form to handle profile creation'''

    class Meta:
        model = Profile
        fields = ['display_name', 'bio_text', 'profile_image', 'cover_image']


#destination forms
class CreateDestinationForm(forms.ModelForm):
    '''a form to add a destination to the database'''

    class Meta:
        '''assoc thsi form with destination model from the database'''
        model = Destination
        fields = ['location', 'arrival_date', 'departure_date', 'cover_image']

class UpdateDestinationForm(forms.ModelForm):
    '''a form to update an existing destination in the database'''

    class Meta:
        '''assoc thsi form with destination model from the database'''
        model = Destination
        fields = ['location', 'arrival_date', 'departure_date', 'cover_image', 'isCompleted']

#journal entry forms
class CreateJournalForm(forms.ModelForm):
    '''a form to add an entry to the database'''

    class Meta:
        '''assoc thsi form with journalentry model from the database'''
        model = JournalEntry
        fields = ['title', 'text']

class UpdateJournalForm(forms.ModelForm):
    '''a form to update an existing entry in the database'''

    class Meta:
        '''assoc thsi form with journalentry model from the database'''
        model = JournalEntry
        fields = ['title', 'text']

#transportation forms
class CreateTransportationForm(forms.ModelForm):
    '''a form to add a transportation to the database'''

    class Meta:
        '''assoc thsi form with transportation model from the database'''
        model = Transportation
        fields = ['location', 'price', 'notes', 'start_datetime', 'end_datetime', 'travel_type', 'final_location']
        labels = {
            'location': 'Departure location',
            'final_location': 'Arrival location',
            'start_datetime': 'Departure time',
            'end_datetime': 'Arrival time',
        }

class UpdateTransportationForm(forms.ModelForm):
    '''a form to update an existing transportation in the database'''

    class Meta:
        '''assoc thsi form with transportation model from the database'''
        model = Transportation
        fields = ['location', 'price', 'notes', 'start_datetime', 'end_datetime', 'travel_type', 'final_location']
        labels = {
            'location': 'Departure location',
            'final_location': 'Arrival location',
            'start_datetime': 'Departure time',
            'end_datetime': 'Arrival time',
        }
        

    
class CreateLodgingForm(forms.ModelForm):
    '''a form to add a lodging to the database'''

    class Meta:
        '''assoc this form with lodging model from the database'''
        model = Lodging
        fields = ['location', 'price', 'notes', 'start_datetime', 'end_datetime']
        labels = {
            'start_datetime': 'Start date',
            'end_datetime': 'End date',
        }

class UpdateLodgingForm(forms.ModelForm):
    '''a form to update an existing lodging in the database'''

    class Meta:
        '''assoc thsi form with lodging model from the database'''
        model = Lodging
        fields = ['location', 'price', 'notes', 'start_datetime', 'end_datetime']
        labels = {
            'start_datetime': 'Start date',
            'end_datetime': 'End date',
        }


class CreateActivityForm(forms.ModelForm):
    '''a form to add a transportation to the database'''

    class Meta:
        '''assoc thsi form with Activity model from the database'''
        model = Activity
        fields = ['location', 'price', 'notes', 'start_datetime', 'end_datetime']
        labels = {
            'start_datetime': 'Start date/time',
            'end_datetime': 'End date/time',
        }

class UpdateActivityForm(forms.ModelForm):
    '''a form to update an existing transportation in the database'''

    class Meta:
        '''assoc thsi form with Activity model from the database'''
        model = Activity
        fields = ['location', 'price', 'notes', 'start_datetime', 'end_datetime']
        labels = {
            'start_datetime': 'Start date/time',
            'end_datetime': 'End date/time',
        }