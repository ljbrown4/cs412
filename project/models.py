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
    
    def get_absolute_url(self):
        return reverse('profile')

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
    
    def get_absolute_url(self):
        return reverse('adventure', args=[self.pk])
    
    #class methods
    def get_destinations(self):
        '''get all destinations associated with this adventure'''
        destinations = Destination.objects.filter(adventure=self).order_by('timestamp')
        return destinations[:6]
    
    def get_all_destinations(self):
        '''get all destinations associated with this adventure'''
        destinations = Destination.objects.filter(adventure=self).order_by('timestamp')
        return destinations
    
    def get_all_itinerary_items(self):
        '''get all itinerary items for this adventure'''
        items = []

        for destination in self.get_destinations():
            items.extend(destination.get_itinerary_items())

        return sorted(items, key=lambda x: x.start_datetime)
    
    def get_packing_list(self):
        '''get 5 packing list items'''
        packing_list = PackingItem.objects.filter(adventure=self).order_by('-timestamp')
        return packing_list[:5]
    
    def get_all_packing_list(self):
        '''get all packing list items''' 
        packing_list = PackingItem.objects.filter(adventure=self).order_by('-timestamp')
        return packing_list

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
    
    def get_absolute_url(self):
        return reverse('destination', args=[self.pk])
    
    #cut offs
    def get_transportation(self):
        '''get all activities for this destination'''
        return Transportation.objects.filter(destination=self).order_by('start_datetime')[:5]

    def get_activities(self):
        '''get all activities for this destination'''
        return Activity.objects.filter(destination=self).order_by('start_datetime')[:6]

    def get_lodging(self):
        '''get all lodging for this destination'''
        return Lodging.objects.filter(destination=self).order_by('start_datetime')[:4]
    
    #all
    def get_all_activities(self):
        '''get all activities for this destination'''
        return Activity.objects.filter(destination=self).order_by('start_datetime')

    def get_all_lodging(self):
        '''get all lodging for this destination'''
        return Lodging.objects.filter(destination=self).order_by('start_datetime')
    
    def get_all_transportation(self):
        '''get all activities for this destination'''
        return Transportation.objects.filter(destination=self).order_by('start_datetime')
    
    def get_entries(self):
        '''get all journal entries associated with this destination'''
        entries = JournalEntry.objects.filter(destination=self).order_by('timestamp')[:4]
        return list(entries)

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
    
    def get_absolute_url(self):
        return reverse('journal', args=[self.pk])
    
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
    caption = models.TextField(blank=True)
    entry = models.ForeignKey(JournalEntry, on_delete=models.CASCADE)
    timestamp = models.DateField(auto_now_add=True) 

    def __str__(self):
        '''return string rep of this destination'''
        return f'{self.media} for entry {self.entry.title}'
    
    #class methods
    def get_media_type(self):
        '''return whether this file is an image or video'''
        name = str(self.media).lower()

        if name.endswith(('.jpg', '.jpeg', '.png')):
            return 'image'
        elif name.endswith(('.mp4', '.avi', '.mov')):
            return 'video'
        return 'other'

class ItineraryItem (models.Model):
    ''' super class for types of itinerary items'''

    #type = models.CharField(max_length=14) #types are transportation, activity, lodging
    location = models.TextField()
    price = models.FloatField()
    notes = models.TextField(blank=True)
    destination = models.ForeignKey(Destination, on_delete=models.CASCADE) 
    start_datetime = models.DateTimeField() 
    end_datetime = models.DateTimeField()
    timestamp = models.DateField(auto_now_add=True)

    class Meta: #for more simplicity
        abstract = True
    

class Transportation(ItineraryItem):
    '''class that encapsulates data for all transportation for a destination'''
    TRAVEL_CHOICES = [('bus', 'Bus'),
        ('taxi', 'Taxi'), ('uber', 'Uber'),
        ('car', 'Car'), ('flight', 'Flight'),
        ('train', 'Train'), ('ferry', 'Ferry'),
        ('other', 'Other'), ]

    travel_type = models.CharField(max_length=20, choices=TRAVEL_CHOICES)
    final_location = models.TextField()

    def __str__(self):
        '''return string rep of this destination'''
        return f'{self.travel_type} for destination {self.destination.location} at {self.start_datetime}'
    
    def get_absolute_url(self):
        return reverse('transportation', args=[self.pk])
    
class Activity(ItineraryItem):
    '''class that encapsulates data for activities for a destination'''

    def __str__(self):
        '''return string rep of this destination'''
        return f'activity for destination {self.destination.location} at {self.location}'
    
    def get_absolute_url(self):
        return reverse('activity', args=[self.pk])

class Lodging(ItineraryItem):
    '''class that encapsulates data for activities for a destination'''

    def __str__(self):
        '''return string rep of this destination'''
        return f'lodging for destination {self.destination.location} at {self.location}'
    
    def get_absolute_url(self):
        return reverse('lodging', args=[self.pk])


class PackingItem(models.Model):
    '''class that encapsulates items user wants to bring with them on the adventure'''

    TYPE_CHOICES = [('clothing', 'Clothing'),
        ('toiletries', 'Toiletries'), ('miscellaneous', 'Miscellaneous'),
        ('electronics', 'Electronics'), ('beauty', 'Beauty'),
        ('health + self care', 'Health + Self Care'), ('trip specific', 'Trip Specific'),
        ('other', 'Other'), ]

    item_type= models.CharField(max_length=20, choices=TYPE_CHOICES)
    item = models.TextField()
    isPacked = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now_add=True)
    notes = models.TextField()
    adventure = models.ForeignKey(Adventure, on_delete=models.CASCADE)

    def __str__(self):
        '''return string rep of this destination'''
        return f'{self.item} for {self.adventure.title}'
