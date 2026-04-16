# File: models.py
# Author: Leigh Brown (ljbrown4@bu.edu), 4/15/2026
# Description: create models and their attributes 

from django.db import models
from django.urls import reverse 
from django.contrib.auth.models import User #for authentication
from django.core.validators import FileExtensionValidator #googled this
# Create your models here.

class Profile(models.Model): 
    ''' Class that encapsulates data for user profiles'''

    display_name = models.TextField(blank=True)
    bio_text = models.TextField(blank=True)
    join_date = models.DateTimeField(auto_now_add=True)
    profile_image = models.ImageField(blank=True)
    cover_image = models.ImageField(blank=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='travel_profile') #looked up how to limit # of users to prevent issue i had with mini insta 

    def __str__(self):
        '''return string rep of this adventure'''
        return f'{self.user.username} created profile on {self.join_date}'

    #class methods
    def get_adventures(self):
        '''return all adventures created by this profile'''
        adventures = Adventure.objects.filter(profile=self).order_by('date_created')
        return adventures

class Adventure (models.Model):
    ''' a class that encapsulates data for a user's trip'''
    title = models.CharField(max_length=100)
    date_created = models.DateTimeField(auto_now_add=True)
    start_date = models.DateField()
    end_date = models.DateField()
    isCompleted = models.BooleanField(default=False)
    budget = models.FloatField()
    cover_image = models.ImageField(blank=True) #users can add a cover image to display with the adventure on the main dashboard
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE) #fk to the profile that created this adventure

    def __str__(self):
        '''return string rep of this adventure'''
        return f'{self.title} created on {self.date_created}'
    
    #class methods
    def get_destinations(self):
        '''get all destinations associated with this adventure'''
        destinations = Destination.objects.filter(adventure=self).order_by('timestamp')
        return destinations
    
    def get_all_itinerary_items(self):
        '''get all itinerary items for this adventure'''
        items = []

        for destination in self.get_destinations():
            items.extend(destination.get_itinerary_items())

        return sorted(items, key=lambda x: x.start_datetime)
    
    def get_all_transportations(self):
        '''get all transportations for this adventure'''
        items = Transportation.objects.none() #initialize 

        for destination in self.get_destinations():
            items = items.union(destination.get_transportation()) #update it by unioning it with the new destinations transportations

        return items.order_by('start_datetime')

class Destination (models.Model):
    '''class that encapsulates data for the destinations a user goes to during their trip'''
    location = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    arrival_date = models.DateField()
    departure_date = models.DateField()
    isCompleted = models.BooleanField(default=False)
    cover_image = models.ImageField(blank=True) #users can add a cover image to display with the destination on the adventure dashboard
    adventure = models.ForeignKey(Adventure, on_delete=models.CASCADE) #fk to adventure it is during
    
    def __str__(self):
        '''return string rep of this destination'''
        return f'{self.location} for adventure {self.adventure.title}'
    
    #class methods
    def get_transportation(self):
        '''get all transportation for this destination'''
        return Transportation.objects.filter(destination=self).order_by('start_datetime')

    def get_activities(self):
        '''get all activities for this destination'''
        return Activity.objects.filter(destination=self).order_by('start_datetime')

    def get_lodging(self):
        '''get all lodging for this destination'''
        return Lodging.objects.filter(destination=self).order_by('start_datetime')
    
    def get_entries(self):
        '''get all journal entries associated with this destination'''
        return JournalEntry.objects.filter(destination=self).order_by('timestamp')
    

    def get_itinerary_items(self):
        '''get all items for this destination's itinerary'''
        items = []

        items.extend(self.get_transportation())
        items.extend(self.get_activities())
        items.extend(self.get_lodging())

        return sorted(items, key=lambda x: x.start_datetime)
    
class JournalEntry (models.Model):
    '''class that encapsulates data for a journal entry associated with a destination'''
    title = models.CharField(max_length=100)
    timestamp = models.DateField(auto_now_add=True)
    text = models.TextField()
    destination = models.ForeignKey(Destination, on_delete=models.CASCADE) 

    def __str__(self):
        '''return string rep of this entry'''
        return f'journal entry: {self.title} for destination {self.destination.location}'
    
    #class methods
    def get_all_media(self):
        '''get all photos for a post'''
        media = Media.objects.filter(entry=self)
        return media

class Media (models.Model):
    ''' class for media uploads associated with a journal entry'''
    media = models.FileField(
        upload_to='project/media/', #have it in a sep folder for organization
        validators=[FileExtensionValidator(allowed_extensions=['mp4', 'avi', 'mov', 'jpg', 'png', 'jpeg'])]
    )
    entry = models.ForeignKey(JournalEntry, on_delete=models.CASCADE) 

    def __str__(self):
        '''return string rep of this destination'''
        return f'{self.media} for entry {self.entry.title}'

class ItineraryItem (models.Model):
    ''' super class for types of itinerary items'''

    #type = models.CharField(max_length=14) #types are transportation, activity, lodging
    location = models.TextField()
    price = models.FloatField()
    notes = models.TextField(blank=True)
    destination = models.ForeignKey(Destination, on_delete=models.CASCADE) 
    start_datetime = models.DateTimeField() 
    end_datetime = models.DateTimeField()

    class Meta: #for more simplicity
        abstract = True

    #class methods
    def get_duration(self): 
        '''return duration of item for display'''
        duration = self.end_datetime - self.start_datetime
        return duration
    

class Transportation(ItineraryItem):
    '''class that encapsulates data for all transportation for a destination'''
    travel_type = models.CharField(max_length=6) #flight, taxi, bus, train, ferry
    final_location = models.TextField()

    def __str__(self):
        '''return string rep of this destination'''
        return f'{self.travel_type} for destination {self.destination.location} at {self.start_datetime}'
    
class Activity(ItineraryItem):
    '''class that encapsulates data for activities for a destination'''

    def __str__(self):
        '''return string rep of this destination'''
        return f'activity for destination {self.destination.location} at {self.location}'

class Lodging(ItineraryItem):
    '''class that encapsulates data for activities for a destination'''

    def __str__(self):
        '''return string rep of this destination'''
        return f'lodging for destination {self.destination.location} at {self.location}'



