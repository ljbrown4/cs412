#File: views.py
# Author: Leigh Brown (ljbrown4@bu.edu), 2/12/2026 + 2/19/2026
# Description: create the functions necessary to connect to html templates

from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView
from .models import *
from django.urls import reverse
from django.shortcuts import render, redirect
from .forms import *
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin 
from django.contrib.auth import login
from django.http import HttpRequest, HttpResponse 
from datetime import date
from collections import OrderedDict #looked this up

# Create your views here.

class ProfileRequiredMixin(LoginRequiredMixin):#loginreqmixin sub class
    """Custom mixin that requires auth and returns user profile as need """
   
    def get_profile(self): 
        """ get profile of current user"""
        return Profile.objects.get(user=self.request.user)
    
    def get_login_url(self):
        return reverse('project_login')
    
class InformationView(ProfileRequiredMixin, TemplateView):
    template_name = 'project/information.html'
    
#profile views
class ProfileDetailView(ProfileRequiredMixin, DetailView):
    '''get profile of current user'''
    model = Profile
    template_name = 'project/profile.html'
    context_object_name = 'profile'

    def get_object(self):
        return self.get_profile()
    
    def get_context_data(self, **kwargs):
        '''return the dict of context variables for use in the template'''
        
        context = super().get_context_data(**kwargs)

        # add to ctxt data, used to display page specific nav icons
        profile = self.get_profile()

        context['profile'] = profile
        context['pfp'] = profile.profile_image
        context['back_url'] = reverse('home')
        
        return context

class UpdateProfileView(ProfileRequiredMixin, UpdateView):
    '''allow users to update profile information'''
    model = Profile
    form_class= UpdateProfileForm
    template_name = "project/update_profile.html"

    def get_object(self):
        return self.get_profile()

    def get_context_data(self, **kwargs):
        '''return the dict of context variables for use in the template'''
        
        context = super().get_context_data(**kwargs)

        # add to ctxt data, used to display page specific nav icons
        context['back_url'] = reverse('profile')
        profile = self.get_profile()

        context['profile'] = profile
        context['pfp'] = profile.profile_image

        return context

class CreateProfileView(CreateView):
    '''view to handle profile creation + user signup'''

    model = Profile
    form_class = CreateProfileForm
    template_name = "project/create_profile.html"

    def form_valid(self, form):
        user_form = UserCreationForm(self.request.POST)

        if not user_form.is_valid():
            context = self.get_context_data(form=form)
            context['user_form'] = user_form
            return self.render_to_response(context)

        # create Django auth user
        new_user = user_form.save()

        # attach profile to auth user
        form.instance.user = new_user

        response = super().form_valid(form)

        # log them in immediately after both user + profile are saved
        login(
            self.request,
            new_user,
            backend='django.contrib.auth.backends.ModelBackend'
        )

        return response

    def get_context_data(self, **kwargs):
        '''add user creation form to template'''
        context = super().get_context_data(**kwargs)

        if 'user_form' not in context:
            context['user_form'] = UserCreationForm()

        context['back_url'] = reverse('project_login')
        return context

    def get_success_url(self):
        '''send user to home page'''
        return reverse('home')
    

#adventure views

class AdventureListView(ProfileRequiredMixin, ListView):
    '''show all adventures created by this profile'''

    model = Adventure
    template_name = 'project/home.html'
    context_object_name = 'adventures'

    def get_queryset(self):
        profile = self.get_profile()
        adventures = profile.get_adventures()

        # get query params
        sort_by = self.request.GET.get('sort', 'created')
        filter_by = self.request.GET.get('filter', 'all')

        today = date.today()

        # filter by progress
        if filter_by == 'completed':
            adventures = adventures.filter(isCompleted=True)
        elif filter_by == 'started':
            adventures = adventures.filter(start_date__lte=today)
        elif filter_by == 'upcoming':
            adventures = adventures.filter(start_date__gt=today)

        # sorting
        if sort_by == 'start':
            adventures = adventures.order_by('start_date')
        else:
            adventures = adventures.order_by('-date_created')

        return adventures
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        profile = self.get_profile()

        context['profile'] = profile
        context['pfp'] = profile.profile_image
        context['cover'] = profile.cover_image

        # current view, sort, and filters applied
        context['current_view'] = self.request.GET.get('view', 'gallery')
        context['current_sort'] = self.request.GET.get('sort', 'created')
        context['current_filter'] = self.request.GET.get('filter', 'all')

        return context

class AdventureDetailView(ProfileRequiredMixin, DetailView):
    '''show details of a specific adventure'''

    model = Adventure
    template_name = 'project/adventure.html'
    context_object_name = 'adventure'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        pk = self.kwargs['pk']
        adventure = Adventure.objects.get(pk=pk)
        destinations = adventure.get_destinations() #views on adventure and destination page from trunchated methods for space reasons
        itinerary = adventure.get_all_itinerary_items()
        packing = adventure.get_packing_list()
        profile = self.get_profile()

        expenses = 0.0
        for i in itinerary:
            expenses += i.price

        #looked this up online so that i could group the itinerary by day
        grouped_itinerary = OrderedDict()

        for item in itinerary:
            day = item.start_datetime.date()

            if day not in grouped_itinerary:
                grouped_itinerary[day] = []

            # figure out item type [get which sub model of itineraryItem it is]
            if isinstance(item, Transportation):
                item_type = 'Transportation'
            elif isinstance(item, Activity):
                item_type = 'Activity'
            else:
                item_type = 'Lodging'

            grouped_itinerary[day].append({
                'item': item,
                'item_type': item_type,
            })

        context['back_url'] = reverse('home')
        context['adventure'] = adventure
        context['profile'] = profile
        context['pfp'] = profile.profile_image 
        context['cover'] = adventure.cover_image    
        context['itinerary'] = grouped_itinerary.items()
        context['destinations'] = destinations
        context['expenses'] = expenses
        context['packing'] = packing
        return context
    
    
class UpdateAdventureView(ProfileRequiredMixin, UpdateView):
    ''' view to handle adventure updates '''
    model = Adventure
    form_class= UpdateAdventureForm
    template_name = "project/update_adventure.html"

    def get_context_data(self, **kwargs):
        #call super
        context = super().get_context_data(**kwargs)

        #get pk
        pk = self.kwargs['pk']
        #find comm obj
        adventure = Adventure.objects.get(pk=pk)

        #add to context data
        profile = self.get_profile()

        context['profile'] = profile
        context['pfp'] = profile.profile_image

        context['back_url'] = reverse('adventure', args=[adventure.pk])
        context['adventure'] = adventure    

        return context

    def get_success_url(self):
        ''' return to profile page upon successful deletion '''
        #find pk 
        pk = self.kwargs['pk']
        #find comm obj
        adventure = Adventure.objects.get(pk=pk)
        return reverse('adventure', kwargs={'pk':adventure.pk})
    
  
class CreateAdventureView(ProfileRequiredMixin, CreateView):
    '''view to handle adventure creation'''

    form_class = CreateAdventureForm
    template_name = 'project/create_adventure.html'

    def form_valid(self, form):
        profile = self.get_profile()
        form.instance.profile = profile
        return super().form_valid(form)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        profile = self.get_profile()

        context['back_url'] = reverse('home')
        context['profile'] = profile

        return context

    def get_success_url(self):
        return reverse('adventure', kwargs={'pk': self.object.pk})


class DeleteAdventureView(ProfileRequiredMixin, DeleteView):
    ''' view to handle adventure deletion '''
    model = Adventure
    template_name = "project/delete_adventure.html"

    def get_context_data(self, **kwargs):
        #call super
        context = super().get_context_data(**kwargs)

        #get pk
        pk = self.kwargs['pk']
        profile = self.get_profile()

        #find comm obj
        adventure = Adventure.objects.get(pk=pk)
        destinations = Destination.objects.filter(adventure__pk=pk)
        transportations = Transportation.objects.filter(destination__adventure__pk=pk)
        activities = Activity.objects.filter(destination__adventure__pk=pk)
        lodgings = Lodging.objects.filter(destination__adventure__pk=pk)
        entries = JournalEntry.objects.filter(destination__adventure__pk=pk)
    
        #add to context data
        context['adventure'] = adventure
        context['destinations'] = destinations
        context['transportations'] = transportations
        context['activities'] = activities
        context['lodgings'] = lodgings
        context['entries'] = entries
        context['back_url'] = reverse('adventure', args=[adventure.pk])
        context['profile'] = profile
        context['pfp'] = profile.profile_image     

        return context

    def get_success_url(self):
        ''' return to home page upon successful deletion'''
        return reverse('home')
    




#destination views
#for specific adventure
class AdventureDestinationListView(ProfileRequiredMixin, ListView):
    '''show all destinations associated with an adventure'''

    model = Destination
    template_name = 'project/destinations.html'
    context_object_name = 'destinations'

    def get_queryset(self):
        pk = self.kwargs['pk']
        adventure = Adventure.objects.get(pk=pk)
        destinations = adventure.get_all_destinations()

        #get query params
        sort_by = self.request.GET.get('sort', 'created')
        filter_by = self.request.GET.get('filter', 'all')

        today = date.today()

        # filter by progress
        if filter_by == 'completed':
            destinations = destinations.filter(isCompleted=True)
        elif filter_by == 'started':
            destinations = destinations.filter(arrival_date__lte=today)
        elif filter_by == 'upcoming':
            destinations = destinations.filter(arrival_date__gt=today)

        # sorting
        if sort_by == 'start':
            destinations = destinations.order_by('arrival_date')
        else:
            destinations = destinations.order_by('-timestamp')

        return destinations
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        pk = self.kwargs['pk']
        adventure = Adventure.objects.get(pk=pk)
        profile = self.get_profile()

        context['pfp'] = profile.profile_image
        context['profile'] = profile
        context['adventure'] = adventure
        context['back_url'] = reverse('adventure', args=[adventure.pk]) #back to the adventure page
        context['current_view'] = self.request.GET.get('view', 'gallery')
        context['current_filter'] = self.request.GET.get('filter', 'all')
        context['current_sort'] = self.request.GET.get('sort', 'created')
        return context
    
#all adventures
class DestinationListView(ProfileRequiredMixin, ListView):
    '''show all destinations associated with an adventure'''

    model = Destination
    template_name = 'project/destinations.html'
    context_object_name = 'destinations'

    def get_queryset(self):
        profile = self.get_profile()

        destinations = Destination.objects.filter(adventure__profile=profile)

        #get query params
        sort_by = self.request.GET.get('sort', 'created')
        filter_by = self.request.GET.get('filter', 'all')

        today = date.today()

        # filter by progress
        if filter_by == 'completed':
            destinations = destinations.filter(isCompleted=True)
        elif filter_by == 'started':
            destinations = destinations.filter(arrival_date__lte=today)
        elif filter_by == 'upcoming':
            destinations = destinations.filter(arrival_date__gt=today)
        #filter by adventure
        elif filter_by not in ['all', 'completed', 'started', 'upcoming']:
            destinations = destinations.filter(adventure__pk=filter_by)

        # sorting
        if sort_by == 'start':
            destinations = destinations.order_by('arrival_date')
        else:
            destinations = destinations.order_by('-timestamp')

        return destinations
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        profile = self.get_profile()
        adventures = Adventure.objects.filter(profile=profile).order_by('title')

        context['pfp'] = profile.profile_image
        context['profile'] = profile
        context['adventures'] = adventures
        context['back_url'] = reverse('home') #back to home page
        context['current_view'] = self.request.GET.get('view', 'gallery')
        context['current_filter'] = self.request.GET.get('filter', 'all')
        context['current_sort'] = self.request.GET.get('sort', 'created')

        return context
    
class DestinationDetailView(ProfileRequiredMixin, DetailView):
    '''show details of a specific destination'''

    model = Destination
    template_name = 'project/destination.html'
    context_object_name = 'destination'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        pk = self.kwargs['pk']
        destination = Destination.objects.get(pk=pk)
        profile = self.get_profile()

        #get all model records for models that have a fk to destination
        transportations = destination.get_transportation()
        itinerary = destination.get_itinerary_items()
        lodgings = destination.get_lodging()
        entries = destination.get_entries()
        activities = destination.get_activities()
        profile = self.get_profile()


        #looked this up online so that i could group the itinerary by day for displaying it in the itinerary portion
        grouped_itinerary = OrderedDict()

        for item in itinerary:
            day = item.start_datetime.date()

            if day not in grouped_itinerary:
                grouped_itinerary[day] = []

            # figure out item type
            if isinstance(item, Transportation):
                item_type = 'Transportation'
            elif isinstance(item, Activity):
                item_type = 'Activity'
            else:
                item_type = 'Lodging'

            grouped_itinerary[day].append({
                'item': item,
                'item_type': item_type,
            })

        context['profile'] = profile
        context['cover'] = destination.cover_image
        context['transportations'] = transportations
        context['back_url'] = reverse('adventure', args=[destination.adventure.pk])
        context['pfp'] = profile.profile_image
        context['destination'] = destination
        context['itinerary'] = grouped_itinerary.items()
        context['lodgings'] = lodgings
        context['entries'] = entries
        context['activities'] = activities

        return context
    
    
class UpdateDestinationView(ProfileRequiredMixin, UpdateView):
    ''' view to handle post updates '''
    model = Destination
    form_class= UpdateDestinationForm
    template_name = "project/update_destination.html"

    def form_valid(self, form):
        pk = self.kwargs['pk']
        destination = Destination.objects.get(pk=pk)
        adventure = destination.adventure

        arrival = form.cleaned_data.get('arrival_date')
        departure = form.cleaned_data.get('departure_date')

        #ensure that date of destination is within the dates of its associated adbenture
        if arrival and arrival < adventure.start_date:
            form.add_error('arrival_date', "Arrival date cannot be before the adventure start date.")
            return self.form_invalid(form)

        if departure and departure > adventure.end_date:
            form.add_error('departure_date', "Departure date cannot be after the adventure end date.")
            return self.form_invalid(form)

        form.instance.adventure = adventure
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        #call super
        context = super().get_context_data(**kwargs)

        #get pk
        pk = self.kwargs['pk']

        #find comm obj
        destination = Destination.objects.get(pk=pk)
        adventure = destination.adventure

        #add to context data
        context['back_url'] = reverse('destination', args=[destination.pk])
        context['destination'] = destination
        context['adventure'] = adventure

        return context

    def get_success_url(self):
        ''' return to profile page upon successful deletion '''
        #find pk 
        pk = self.kwargs['pk']
        #find comm obj
        destination = Destination.objects.get(pk=pk)
        return reverse('destination', kwargs={'pk':destination.pk})
    
  
class CreateDestinationView(ProfileRequiredMixin, CreateView):
    '''view to handle destination creation'''

    form_class = CreateDestinationForm
    template_name = 'project/create_destination.html'

    def form_valid(self, form):
        pk = self.kwargs['pk']
        adventure = Adventure.objects.get(pk=pk)

        arrival = form.cleaned_data.get('arrival_date')
        departure = form.cleaned_data.get('departure_date')
        
        #ensure that date of destination is within the dates of its associated adventure
        if arrival and arrival < adventure.start_date:
            form.add_error('arrival_date', "Arrival date cannot be before the adventure start date.")
            return self.form_invalid(form)

        if departure and departure > adventure.end_date:
            form.add_error('departure_date', "Departure date cannot be after the adventure end date.")
            return self.form_invalid(form)

        form.instance.adventure = adventure
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        pk = self.kwargs['pk']
        adventure = Adventure.objects.get(pk=pk)
        profile = self.get_profile()

        context['pfp'] = profile.profile_image
        context['profile'] = profile
        context['back_url'] = reverse('adventure', args=[adventure.pk])
        context['adventure'] = adventure

        return context

    def get_success_url(self):
        return reverse('adventure', args=[self.object.adventure.pk])

class DeleteDestinationView(ProfileRequiredMixin, DeleteView):
    ''' view to handle destination deletion '''
    model = Destination
    template_name = "project/delete_destination.html"

    def get_context_data(self, **kwargs):
        #call super
        context = super().get_context_data(**kwargs)

        #get pk
        pk = self.kwargs['pk']

        #find comm obj
        destination = Destination.objects.get(pk=pk)
        transportations = Transportation.objects.filter(destination__pk=pk)
        activities = Activity.objects.filter(destination__pk=pk)
        lodgings = Lodging.objects.filter(destination__pk=pk)
        entries = JournalEntry.objects.filter(destination__pk=pk)
    
        #add to context data
        profile = self.get_profile()

        context['pfp'] = profile.profile_image
        context['profile'] = profile
        context['destination'] = destination
        context['transportations'] = transportations
        context['activities'] = activities
        context['lodgings'] = lodgings
        context['entries'] = entries
        context['back_url'] = reverse('destination', args=[destination.pk])     

        return context

    def get_success_url(self):
        ''' return to home page upon successful deletion'''
        pk = self.kwargs['pk']
        destination = Destination.objects.get(pk=pk)
        return reverse('adventure', args=[destination.adventure.pk])
    




#journal views
#PER DESTINATION
class DestinationJournalListView(ProfileRequiredMixin, ListView):
    '''show all journals associated with an destination'''

    model = JournalEntry
    template_name = 'project/journals.html'
    context_object_name = 'journals'

    def get_queryset(self):
        pk = self.kwargs['pk']
        destination = Destination.objects.get(pk=pk)
        journals = destination.get_entries()

        return journals
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        pk = self.kwargs['pk']

        profile = self.get_profile()
        destination = Destination.objects.get(pk=pk)


        context['pfp'] = profile.profile_image
        context['profile'] = profile
        context['destination'] = destination
        context['back_url'] = reverse('destination', args=[destination.pk]) #back to the destination page
        context['current_view'] = self.request.GET.get('view', 'gallery')
        return context

#ALL ENTRIES   
class JournalListView(ProfileRequiredMixin, ListView):
    '''show all journals associated with an destination'''

    model = JournalEntry
    template_name = 'project/journals.html'
    context_object_name = 'journals'

    def get_queryset(self):
        profile = self.get_profile()

        journals = JournalEntry.objects.filter(destination__adventure__profile=profile)

        filter_by = self.request.GET.get('filter', 'all')

        #filter by destination
        if filter_by != 'all':
            journals = journals.filter(destination__pk=filter_by)

        return journals
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        profile = self.get_profile()
        # all destinations created by this user for dropdown filter
        destinations = Destination.objects.filter(adventure__profile=profile).order_by('location')


        context['pfp'] = profile.profile_image
        context['profile'] = profile
        context['destinations'] = destinations
        context['back_url'] = reverse('home') #back to home page
        context['current_filter'] = self.request.GET.get('filter', 'all')
        context['current_view'] = self.request.GET.get('view', 'gallery')
        return context
    
class JournalDetailView(ProfileRequiredMixin, DetailView):
    '''show details of a specific journal'''

    model = JournalEntry
    template_name = 'project/journal.html'
    context_object_name = 'journal'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        profile = self.get_profile()
        pk = self.kwargs['pk']
        journal = JournalEntry.objects.get(pk=pk)

        context['profile'] = profile
        context['pfp'] = profile.profile_image
        context['journal'] = journal
        context['back_url'] = reverse('destination', args=[journal.destination.pk])
        context['pfp'] = profile.profile_image     

        return context   
    
class UpdateJournalView(ProfileRequiredMixin, UpdateView):
    ''' view to handle journal updates '''
    model = JournalEntry
    form_class= UpdateJournalForm
    template_name = "project/update_journal.html"

    def get_context_data(self, **kwargs):
        #call super
        context = super().get_context_data(**kwargs)

        #get pk
        pk = self.kwargs['pk']

        #find comm obj
        journal = JournalEntry.objects.get(pk=pk)

        #add to context data
        profile = self.get_profile()

        context['pfp'] = profile.profile_image
        context['profile'] = profile
        context['back_url'] = reverse('journal', args=[journal.pk])
        context['journal'] = journal

        return context

    def get_success_url(self):
        ''' return to profile page upon successful deletion '''
        #find pk 
        pk = self.kwargs['pk']
        #find comm obj
        journal = JournalEntry.objects.get(pk=pk)
        return reverse('journal', kwargs={'pk':journal.pk})
    
  
class CreateJournalView(ProfileRequiredMixin, CreateView):
    '''view to handle journal creation'''

    form_class = CreateJournalForm
    template_name = 'project/create_journal.html'

    def form_valid(self, form):
        pk = self.kwargs['pk']
        destination = Destination.objects.get(pk=pk)

        form.instance.destination = destination

        response = super().form_valid(form)

        for file in self.request.FILES.getlist('media'):
            Media.objects.create(
                entry=self.object,
                media=file
            )
        return response

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        pk = self.kwargs['pk']
        destination = Destination.objects.get(pk=pk)
        profile = self.get_profile()

        context['pfp'] = profile.profile_image
        context['profile'] = profile
        context['destination'] = destination
        context['back_url'] = reverse('destination', args=[destination.pk])

        return context

    def get_success_url(self):
        pk = self.kwargs['pk']
        destination = Destination.objects.get(pk=pk)
        return reverse('destination', args=[destination.pk])


class DeleteJournalView(ProfileRequiredMixin, DeleteView):
    ''' view to handle journal deletion '''
    model = JournalEntry
    template_name = "project/delete_journal.html"

    def get_context_data(self, **kwargs):
        #call super
        context = super().get_context_data(**kwargs)

        #get pk
        pk = self.kwargs['pk']

        #find comm obj
        journal = JournalEntry.objects.get(pk=pk)
    
        #add to context data
        profile = self.get_profile()

        context['pfp'] = profile.profile_image
        context['profile'] = profile
        context['journal'] = journal
        context['back_url'] = reverse('destination', args=[journal.destination.pk])     

        return context

    def get_success_url(self):
        ''' return to destination page upon successful deletion'''
        pk = self.kwargs['pk']
        journal = JournalEntry.objects.get(pk=pk)
        return reverse('destination', args=[journal.destination.pk])





#media views
class MediaDetailView(ProfileRequiredMixin, DetailView):
    '''show details of a specific media item'''

    model = Media
    template_name = 'project/media.html'
    context_object_name = 'media'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        profile = self.get_profile()
        pk = self.kwargs['pk']
        media = Media.objects.get(pk=pk)

        context['profile'] = profile
        context['media'] = media
        context['back_url'] = reverse('journal', args=[media.entry.pk])
        context['pfp'] = profile.profile_image     

        return context
    
class CreateMediaView(ProfileRequiredMixin, CreateView):
    '''view to handle media creation'''

    form_class = CreateMediaForm
    template_name = 'project/create_media.html'

    def form_valid(self, form):
        pk = self.kwargs['pk']
        journal = JournalEntry.objects.get(pk=pk)

        form.instance.entry = journal
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        pk = self.kwargs['pk']
        journal = JournalEntry.objects.get(pk=pk)
        profile = self.get_profile()

        context['pfp'] = profile.profile_image
        context['profile'] = profile
        context['journal'] = journal
        context['back_url'] = reverse('journal', args=[journal.pk])

        return context

    def get_success_url(self):
        pk = self.kwargs['pk']
        journal = JournalEntry.objects.get(pk=pk)
        return reverse('journal', args=[journal.pk])


class DeleteMediaView(ProfileRequiredMixin, DeleteView):
    ''' view to handle media deletion '''
    model = Media
    template_name = "project/delete_media.html"

    def get_context_data(self, **kwargs):
        #call super
        context = super().get_context_data(**kwargs)

        #get pk
        pk = self.kwargs['pk']

        #find comm obj
        media = Media.objects.get(pk=pk)
        journal = media.entry
    
        #add to context data
        profile = self.get_profile()

        context['pfp'] = profile.profile_image
        context['profile'] = profile
        context['media'] = media
        context['back_url'] = reverse('journal', args=[journal.pk])     

        return context

    def get_success_url(self):
        ''' return to journal page upon successful deletion'''
        pk = self.kwargs['pk']
        media = Media.objects.get(pk=pk)
        journal = media.entry
        return reverse('journal', args=[journal.pk])
    
#transportation views
class TransportationListView(ProfileRequiredMixin, ListView):
    '''show all transportation associated with a destination'''

    model = Transportation
    template_name = 'project/transportations.html'
    context_object_name = 'transportations'

    def get_queryset(self):
        pk = self.kwargs['pk']
        destination = Destination.objects.get(pk=pk)
        return destination.get_all_transportation()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        pk = self.kwargs['pk']
        profile = self.get_profile()
        destination = Destination.objects.get(pk=pk)
        transportations = destination.get_all_transportation()

        filter_by = self.request.GET.get('filter', 'all')

        today = date.today()

        # filters
        #filter by departure date
        if filter_by == 'passed':
            transportations = transportations.filter(start_datetime__date__lte=today)
        if filter_by == 'upcoming':
            transportations = transportations.filter(start_datetime__date__gt=today)

        # filter by travel type
        if filter_by == 'bus':
            transportations = transportations.filter(travel_type='bus')
        elif filter_by == 'taxi':
            transportations = transportations.filter(travel_type='taxi')
        elif filter_by == 'uber':
            transportations = transportations.filter(travel_type='uber')
        elif filter_by == 'car':
            transportations = transportations.filter(travel_type='car')
        elif filter_by == 'flight':
            transportations = transportations.filter(travel_type='flight')
        elif filter_by == 'train':
            transportations = transportations.filter(travel_type='train')
        elif filter_by == 'ferry':
            transportations = transportations.filter(travel_type='ferry')
        elif filter_by == 'other':
            transportations = transportations.filter(travel_type='other')

        context['pfp'] = profile.profile_image
        context['profile'] = profile
        context['destination'] = destination
        context['transportations'] = transportations
        context['back_url'] = reverse('destination', args=[destination.pk])
        context['current_view'] = self.request.GET.get('view', 'gallery')
        context['current_filter'] = self.request.GET.get('filter', 'all')

        return context
    
class TransportationDetailView(ProfileRequiredMixin, DetailView):
    '''show details of a specific transportation item'''

    model = Transportation
    template_name = 'project/transportation.html'
    context_object_name = 'transportation'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        pk = self.kwargs['pk']
        transportation = Transportation.objects.get(pk=pk)
        profile = self.get_profile()

        context['profile'] = profile
        context['transportation'] = transportation
        context['back_url'] = reverse('destination', args=[transportation.destination.pk])
        context['pfp'] = profile.profile_image

        return context

class CreateTransportationView(ProfileRequiredMixin, CreateView):
    '''view to handle transportation creation'''

    form_class = CreateTransportationForm
    template_name = 'project/create_transportation.html'

    def form_valid(self, form):
        pk = self.kwargs['pk']
        destination = Destination.objects.get(pk=pk)

        start = form.cleaned_data.get('start_datetime')
        end = form.cleaned_data.get('end_datetime')

        #ensure that date of transp is within the dates of its associated destination
        if start and start.date() < destination.arrival_date:
            form.add_error('start_datetime', "Start date cannot be before the destination arrival date.")
            return self.form_invalid(form)

        if end and end.date() > destination.departure_date:
            form.add_error('end_datetime', "End date cannot be after the destination departure date.")
            return self.form_invalid(form)

        form.instance.destination = destination
        return super().form_valid(form)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        pk = self.kwargs['pk']
        destination = Destination.objects.get(pk=pk)
        profile = self.get_profile()

        context['pfp'] = profile.profile_image
        context['profile'] = profile
        context['destination'] = destination
        context['back_url'] = reverse('destination', args=[destination.pk])

        return context

    def get_success_url(self):
        pk = self.kwargs['pk']
        destination = Destination.objects.get(pk=pk)
        return reverse('destination', args=[destination.pk])

    
    
class UpdateTransportationView(ProfileRequiredMixin, UpdateView):
    '''view to handle transportation updates'''

    model = Transportation
    form_class = UpdateTransportationForm
    template_name = 'project/update_transportation.html'

    def form_valid(self, form):
        transportation = self.get_object()
        destination = transportation.destination

        start = form.cleaned_data.get('start_datetime')
        end = form.cleaned_data.get('end_datetime')

        #ensure that date of transp is within the dates of its associated destination
        if start and start.date() < destination.arrival_date:
            form.add_error('start_datetime', "Start date cannot be before the destination arrival date.")
            return self.form_invalid(form)

        if end and end.date() > destination.departure_date:
            form.add_error('end_datetime', "End date cannot be after the destination departure date.")
            return self.form_invalid(form)

        form.instance.destination = destination
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        pk = self.kwargs['pk']
        transportation = Transportation.objects.get(pk=pk)
        profile = self.get_profile()

        context['pfp'] = profile.profile_image
        context['profile'] = profile
        context['back_url'] = reverse('transportation', args=[transportation.pk])
        context['transportation'] = transportation

        return context

    def get_success_url(self):
        pk = self.kwargs['pk']
        transportation = Transportation.objects.get(pk=pk)
        return reverse('transportation', kwargs={'pk': transportation.pk})
    
class DeleteTransportationView(ProfileRequiredMixin, DeleteView):
    '''view to handle transportation deletion'''

    model = Transportation
    template_name = 'project/delete_transportation.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        pk = self.kwargs['pk']
        transportation = Transportation.objects.get(pk=pk)
        profile = self.get_profile()

        context['pfp'] = profile.profile_image
        context['profile'] = profile
        context['transportation'] = transportation
        context['back_url'] = reverse('destination', args=[transportation.destination.pk])

        return context

    def get_success_url(self):
        pk = self.kwargs['pk']
        transportation = Transportation.objects.get(pk=pk)
        return reverse('destination', args=[transportation.destination.pk])
    
#lodging views
class LodgingListView(ProfileRequiredMixin, ListView):
    '''show all lodging associated with a destination'''

    model = Lodging
    template_name = 'project/lodgings.html'
    context_object_name = 'lodgings'

    def get_queryset(self):
        pk = self.kwargs['pk']
        destination = Destination.objects.get(pk=pk)
        return destination.get_all_lodging()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        pk = self.kwargs['pk']
        profile = self.get_profile()
        destination = Destination.objects.get(pk=pk)

        context['profile'] = profile
        context['pfp'] = profile.profile_image
        context['destination'] = destination
        context['back_url'] = reverse('destination', args=[destination.pk])
        context['current_view'] = self.request.GET.get('view', 'gallery')

        return context
    
class LodgingDetailView(ProfileRequiredMixin, DetailView):
    '''show details of a specific lodging item'''

    model = Lodging
    template_name = 'project/lodging.html'
    context_object_name = 'lodging'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        pk = self.kwargs['pk']
        lodging = Lodging.objects.get(pk=pk)
        profile = self.get_profile()

        context['profile'] = profile
        context['lodging'] = lodging
        context['back_url'] = reverse('destination', args=[lodging.destination.pk])
        context['pfp'] = profile.profile_image

        return context

class CreateLodgingView(ProfileRequiredMixin, CreateView):
    '''view to handle lodging creation'''

    form_class = CreateLodgingForm
    template_name = 'project/create_lodging.html'

    def form_valid(self, form):
        pk = self.kwargs['pk']
        destination = Destination.objects.get(pk=pk)

        start = form.cleaned_data.get('start_datetime')
        end = form.cleaned_data.get('end_datetime')

        #ensure that date of lodging is within the dates of its associated destination
        if start and start.date() < destination.arrival_date:
            form.add_error('start_datetime', "Start date cannot be before the destination arrival date.")
            return self.form_invalid(form)

        if end and end.date() > destination.departure_date:
            form.add_error('end_datetime', "End date cannot be after the destination departure date.")
            return self.form_invalid(form)

        form.instance.destination = destination
        return super().form_valid(form)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        pk = self.kwargs['pk']
        destination = Destination.objects.get(pk=pk)
        profile = self.get_profile()

        context['pfp'] = profile.profile_image
        context['profile'] = profile
        context['destination'] = destination
        context['back_url'] = reverse('destination', args=[destination.pk])

        return context

    def get_success_url(self):
        pk = self.kwargs['pk']
        destination = Destination.objects.get(pk=pk)
        return reverse('destination', args=[destination.pk])

class UpdateLodgingView(ProfileRequiredMixin, UpdateView):
    '''view to handle lodging updates'''

    model = Lodging
    form_class = UpdateLodgingForm
    template_name = 'project/update_lodging.html'

    def form_valid(self, form):
        lodging = self.get_object()
        destination = lodging.destination

        start = form.cleaned_data.get('start_datetime')
        end = form.cleaned_data.get('end_datetime')

        #ensure that date of lodging is within the dates of its associated destination
        if start and start.date() < destination.arrival_date:
            form.add_error('start_datetime', "Start date cannot be before the destination arrival date.")
            return self.form_invalid(form)

        if end and end.date() > destination.departure_date:
            form.add_error('end_datetime', "End date cannot be after the destination departure date.")
            return self.form_invalid(form)

        form.instance.destination = destination
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        pk = self.kwargs['pk']
        lodging = Lodging.objects.get(pk=pk)
        profile = self.get_profile()

        context['pfp'] = profile.profile_image
        context['profile'] = profile
        context['back_url'] = reverse('lodging', args=[lodging.pk])
        context['lodging'] = lodging

        return context

    def get_success_url(self):
        pk = self.kwargs['pk']
        lodging = Lodging.objects.get(pk=pk)
        return reverse('lodging', kwargs={'pk': lodging.pk})
    
class DeleteLodgingView(ProfileRequiredMixin, DeleteView):
    '''view to handle lodging deletion'''

    model = Lodging
    template_name = 'project/delete_lodging.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        pk = self.kwargs['pk']
        lodging = Lodging.objects.get(pk=pk)
        profile = self.get_profile()

        context['pfp'] = profile.profile_image
        context['profile'] = profile
        context['lodging'] = lodging
        context['back_url'] = reverse('destination', args=[lodging.destination.pk])

        return context

    def get_success_url(self):
        pk = self.kwargs['pk']
        lodging = Lodging.objects.get(pk=pk)
        return reverse('destination', args=[lodging.destination.pk])
    
#activity views
class ActivityListView(ProfileRequiredMixin, ListView):
    '''show all activity associated with a destination'''

    model = Activity
    template_name = 'project/activities.html'
    context_object_name = 'activities'

    def get_queryset(self):
        pk = self.kwargs['pk']
        destination = Destination.objects.get(pk=pk)
        return destination.get_all_activities()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        pk = self.kwargs['pk']
        profile = self.get_profile()
        destination = Destination.objects.get(pk=pk)

        context['profile'] = profile
        context['pfp'] = profile.profile_image
        context['destination'] = destination
        context['back_url'] = reverse('destination', args=[destination.pk])
        context['current_view'] = self.request.GET.get('view', 'gallery')

        return context
    
class ActivityDetailView(ProfileRequiredMixin, DetailView):
    '''show details of a specific activity item'''

    model = Activity
    template_name = 'project/activity.html'
    context_object_name = 'activity'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        pk = self.kwargs['pk']
        activity = Activity.objects.get(pk=pk)
        profile = self.get_profile()

        context['profile'] = profile
        context['activity'] = activity
        context['back_url'] = reverse('destination', args=[activity.destination.pk])
        context['pfp'] = profile.profile_image

        return context

class CreateActivityView(ProfileRequiredMixin, CreateView):
    '''view to handle activity creation'''

    form_class = CreateActivityForm
    template_name = 'project/create_activity.html'

    def form_valid(self, form):
        pk = self.kwargs['pk']
        destination = Destination.objects.get(pk=pk)

        start = form.cleaned_data.get('start_datetime')
        end = form.cleaned_data.get('end_datetime')

        #ensure that date of activity is within the dates of its associated destination
        if start and start.date() < destination.arrival_date:
            form.add_error('start_datetime', "Start date cannot be before the destination arrival date.")
            return self.form_invalid(form)

        if end and end.date() > destination.departure_date:
            form.add_error('end_datetime', "End date cannot be after the destination departure date.")
            return self.form_invalid(form)

        form.instance.destination = destination
        return super().form_valid(form)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        pk = self.kwargs['pk']
        destination = Destination.objects.get(pk=pk)
        profile = self.get_profile()

        context['pfp'] = profile.profile_image
        context['profile'] = profile
        context['destination'] = destination
        context['back_url'] = reverse('destination', args=[destination.pk])

        return context

    def get_success_url(self):
        pk = self.kwargs['pk']
        destination = Destination.objects.get(pk=pk)
        return reverse('destination', args=[destination.pk])

    
class UpdateActivityView(ProfileRequiredMixin, UpdateView):
    '''view to handle activity updates'''

    model = Activity
    form_class = UpdateActivityForm
    template_name = 'project/update_activity.html'

    def form_valid(self, form):
        activity = self.get_object()
        destination = activity.destination

        #ensure that date of activity is within the dates of its associated destination
        start = form.cleaned_data.get('start_datetime')
        end = form.cleaned_data.get('end_datetime')

        if start and start.date() < destination.arrival_date:
            form.add_error('start_datetime', "Start date cannot be before the destination arrival date.")
            return self.form_invalid(form)

        if end and end.date() > destination.departure_date:
            form.add_error('end_datetime', "End date cannot be after the destination departure date.")
            return self.form_invalid(form)

        form.instance.destination = destination
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        pk = self.kwargs['pk']
        activity = Activity.objects.get(pk=pk)
        profile = self.get_profile()

        context['pfp'] = profile.profile_image
        context['profile'] = profile
        context['back_url'] = reverse('activity', args=[activity.pk])
        context['activity'] = activity

        return context

    def get_success_url(self):
        pk = self.kwargs['pk']
        activity = Activity.objects.get(pk=pk)
        return reverse('activity', kwargs={'pk': activity.pk})
    
class DeleteActivityView(ProfileRequiredMixin, DeleteView):
    '''view to handle activity deletion'''

    model = Activity
    template_name = 'project/delete_activity.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        pk = self.kwargs['pk']
        activity = Activity.objects.get(pk=pk)
        profile = self.get_profile()

        context['pfp'] = profile.profile_image
        context['profile'] = profile
        context['activity'] = activity
        context['back_url'] = reverse('destination', args=[activity.destination.pk])

        return context

    def get_success_url(self):
        pk = self.kwargs['pk']
        activity = Activity.objects.get(pk=pk)
        return reverse('destination', args=[activity.destination.pk])
    




#packing views
class PackingListView(ProfileRequiredMixin, ListView):
    '''show all packing items associated with an adventure'''

    model = PackingItem
    template_name = 'project/packing_list.html'
    context_object_name = 'packing'

    def get_queryset(self):
        pk = self.kwargs['pk']
        adventure = Adventure.objects.get(pk=pk)
        packing = adventure.get_all_packing_list()

        #filters
        filter_by = self.request.GET.get('filter', 'all')
        #filter by item type
        if filter_by == 'clothing':
           packing = packing.filter(item_type='clothing')
        elif filter_by == 'toiletries':
            packing = packing.filter(item_type='toiletries')
        elif filter_by == 'miscellaneous':
            packing = packing.filter(item_type='miscellaneous')
        elif filter_by == 'electronics':
            packing = packing.filter(item_type='electronics')
        elif filter_by == 'beauty':
            packing = packing.filter(item_type='beauty')
        elif filter_by == 'health + self care':
            packing = packing.filter(item_type='health + self care')
        elif filter_by == 'trip specific':
            packing = packing.filter(item_type='trip specific')
        elif filter_by == 'other':
            packing = packing.filter(item_type='other')

        # filter by packed or unpacked
        if filter_by == 'packed':
            packing = packing.filter(isPacked=True)
        elif filter_by == 'unpacked':
            packing = packing.filter(isPacked=False)

        return packing
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        pk = self.kwargs['pk']
        adventure = Adventure.objects.get(pk=pk)
        profile = self.get_profile()

        context['profile'] = profile
        context['pfp'] = profile.profile_image
        context['adventure'] = adventure
        context['back_url'] = reverse('adventure', args=[adventure.pk]) #back to the adventure page
        context['current_view'] = self.request.GET.get('view', 'gallery')
        context['current_filter'] = self.request.GET.get('filter', 'all')
        return context
    
class PackingDetailView(ProfileRequiredMixin, DetailView):
    '''show details of a specific packing item'''

    model = PackingItem
    template_name = 'project/packing_item.html'
    context_object_name = 'item'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        pk = self.kwargs['pk']
        packing = PackingItem.objects.get(pk=pk)
        profile = self.get_profile()

        context['profile'] = profile
        context['transportation'] = packing
        context['back_url'] = reverse('adventure', args=[packing.adventure.pk])
        context['pfp'] = profile.profile_image

        return context

class UpdatePackingView(ProfileRequiredMixin, UpdateView):
    ''' view to handle packing updates '''
    model = PackingItem
    form_class= UpdatePackingForm
    template_name = "project/update_item.html"

    def get_context_data(self, **kwargs):
        #call super
        context = super().get_context_data(**kwargs)

        #get pk
        pk = self.kwargs['pk']

        #find comm obj
        item = PackingItem.objects.get(pk=pk)
        adventure = item.adventure

        #add to context data
        profile = self.get_profile()

        context['pfp'] = profile.profile_image
        context['profile'] = profile
        context['back_url'] = reverse('packing_item', args=[item.pk])
        context['adventure'] = adventure
        context['item'] = item

        return context

    def get_success_url(self):
        ''' return to packing page upon successful deletion '''
        #find pk 
        pk = self.kwargs['pk']
        #find comm obj
        item = PackingItem.objects.get(pk=pk)
        return reverse('packing_item', kwargs={'pk':item.pk})
    
  
class CreatePackingView(ProfileRequiredMixin, CreateView):
    '''view to handle packing creation'''

    form_class = CreatePackingForm
    template_name = 'project/create_item.html'

    def form_valid(self,form):
        pk = self.kwargs['pk']
        adventure = Adventure.objects.get(pk=pk)

        form.instance.adventure = adventure
        return super().form_valid(form) 
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        pk = self.kwargs['pk']
        adventure = Adventure.objects.get(pk=pk)
        profile = self.get_profile()

        context['pfp'] = profile.profile_image
        context['profile'] = profile
        context['back_url'] = reverse('adventure', args=[adventure.pk])
        context['adventure'] = adventure

        return context

    def get_success_url(self):
        pk = self.kwargs['pk']
        adventure = Adventure.objects.get(pk=pk)
        return reverse('adventure', args=[adventure.pk])

class DeletePackingView(ProfileRequiredMixin, DeleteView):
    ''' view to handle packing deletion '''
    model = PackingItem
    template_name = "project/delete_item.html"

    def get_context_data(self, **kwargs):
        #call super
        context = super().get_context_data(**kwargs)

        #get pk
        pk = self.kwargs['pk']

        #find comm obj
        item = PackingItem.objects.get(pk=pk)
    
        #add to context data
        profile = self.get_profile()

        context['pfp'] = profile.profile_image
        context['profile'] = profile
        context['item'] = item
        context['back_url'] = reverse('adventure', args=[item.adventure.pk])     

        return context

    def get_success_url(self):
        ''' return to adventure page upon successful deletion'''
        pk = self.kwargs['pk']
        packing = PackingItem.objects.get(pk=pk)
        return reverse('adventure', args=[packing.adventure.pk])
    