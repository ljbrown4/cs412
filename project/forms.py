# File: forms.py
# Author: Leigh Brown (ljbrown4@bu.edu), 4/15/2026
# Description: create forms and their fields 

from django import forms
from .models import *
from django.core.exceptions import ValidationError #looked up online how to raise errors for incorrect date input

#adventure forms
class CreateAdventureForm(forms.ModelForm):
    '''a form to add an adventure to the database'''

    class Meta:
        '''assoc thsi form with adventure model from the database'''
        model = Adventure
        fields = ['title', 'start_date', 'end_date', 'budget', 'cover_image']
        widgets = { #looked up online how to get the calendar for this
            'start_date': forms.DateInput(attrs={'type': 'date'}),
            'end_date': forms.DateInput(attrs={'type': 'date'}),
        }

    def clean(self):
        cleaned_data = super().clean()

        start = cleaned_data.get('start_date')
        end = cleaned_data.get('end_date')

        if start and end and end < start:
            raise ValidationError("End date cannot be before start date.")

        return cleaned_data

class UpdateAdventureForm(forms.ModelForm):
    '''a form to add an adventure to the database'''

    class Meta:
        '''assoc thsi form with adventure model from the database'''
        model = Adventure
        fields = ['title', 'start_date', 'end_date', 'budget', 'cover_image', 'isCompleted']
        widgets = {
            'start_date': forms.DateInput(attrs={'type': 'date'}),
            'end_date': forms.DateInput(attrs={'type': 'date'}),
        }
        labels = {
            'isCompleted': 'Adventure Completed',
        }

    def clean(self):
            cleaned_data = super().clean()

            start = cleaned_data.get('start_date')
            end = cleaned_data.get('end_date')

            if start and end and end < start:
                raise ValidationError("End date cannot be before start date.")

            return cleaned_data


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
        widgets = { #looked up online how to get the calendar for this
            'arrival_date': forms.DateInput(attrs={'type': 'date'}),
            'departure_date': forms.DateInput(attrs={'type': 'date'}),
        }

    def clean(self):
        cleaned_data = super().clean()

        arrival = cleaned_data.get('arrival_date')
        departure = cleaned_data.get('departure_date')

        if arrival and departure and departure < arrival:
            self.add_error('departure_date', "Departure date cannot be before arrival date.")

        return cleaned_data

class UpdateDestinationForm(forms.ModelForm):
    '''a form to update an existing destination in the database'''

    class Meta:
        '''assoc thsi form with destination model from the database'''
        model = Destination
        fields = ['location', 'arrival_date', 'departure_date', 'cover_image', 'isCompleted']
        widgets = { #looked up online how to get the calendar for this
            'arrival_date': forms.DateInput(attrs={'type': 'date'}),
            'departure_date': forms.DateInput(attrs={'type': 'date'}),
        }

    def clean(self):
        cleaned_data = super().clean()

        arrival = cleaned_data.get('arrival_date')
        departure = cleaned_data.get('departure_date')

        if arrival and departure and departure < arrival:
            self.add_error('departure_date', "Departure date cannot be before arrival date.")

        return cleaned_data

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

#media forms
class CreateMediaForm(forms.ModelForm):
    '''form to handle media creation'''

    class Meta:
        model = Media
        fields = ['media', 'caption']

#transportation forms
class CreateTransportationForm(forms.ModelForm):
    '''a form to add a transportation to the database'''

    class Meta:
        '''assoc thsi form with transportation model from the database'''
        model = Transportation
        fields = ['location', 'final_location', 'price', 'notes', 'start_datetime', 'end_datetime', 'travel_type', ]
        labels = {
            'location': 'Departure location',
            'final_location': 'Arrival location',
            'start_datetime': 'Departure time',
            'end_datetime': 'Arrival time',
        }
        widgets = {
            'start_datetime': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'end_datetime': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }

    def clean(self):
        cleaned_data = super().clean()

        start = cleaned_data.get('start_datetime')
        end = cleaned_data.get('start_datetime')

        if start and end and end < start:
            raise ValidationError("Departrure date cannot be before arrival date.")

        return cleaned_data

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
        widgets = {
            'start_datetime': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'end_datetime': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }

    def clean(self):
        cleaned_data = super().clean()

        start = cleaned_data.get('start_datetime')
        end = cleaned_data.get('start_datetime')

        if start and end and end < start:
            raise ValidationError("Departrure date cannot be before arrival date.")

        return cleaned_data

    
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
        widgets = {
            'start_datetime': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'end_datetime': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }

    def clean(self):
            cleaned_data = super().clean()

            start = cleaned_data.get('start_datetime')
            end = cleaned_data.get('start_datetime')

            if start and end and end < start:
                raise ValidationError("Departrure date cannot be before arrival date.")

            return cleaned_data

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
        widgets = {
            'start_datetime': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'end_datetime': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }

    def clean(self):
            cleaned_data = super().clean()

            start = cleaned_data.get('start_datetime')
            end = cleaned_data.get('start_datetime')

            if start and end and end < start:
                raise ValidationError("Departrure date cannot be before arrival date.")

            return cleaned_data


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
        widgets = {
            'start_datetime': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'end_datetime': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }

    def clean(self):
            cleaned_data = super().clean()

            start = cleaned_data.get('start_datetime')
            end = cleaned_data.get('start_datetime')

            if start and end and end < start:
                raise ValidationError("Departrure date cannot be before arrival date.")

            return cleaned_data

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
        widgets = {
            'start_datetime': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'end_datetime': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }
        
    def clean(self):
            cleaned_data = super().clean()

            start = cleaned_data.get('start_datetime')
            end = cleaned_data.get('start_datetime')

            if start and end and end < start:
                raise ValidationError("Departrure date cannot be before arrival date.")

            return cleaned_data

#packing forms
class CreatePackingForm(forms.ModelForm):
    '''a form to add an entry to the database'''

    class Meta:
        '''assoc thsi form with journalentry model from the database'''
        model = PackingItem
        fields = ['item_type', 'item', 'notes']

class UpdatePackingForm(forms.ModelForm):
    '''a form to update an existing entry in the database'''

    class Meta:
        '''assoc thsi form with journalentry model from the database'''
        model = PackingItem
        fields = ['item_type', 'item', 'notes', 'isPacked']