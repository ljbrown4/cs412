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

# Create your views here.

class ProfileRequiredMixin(LoginRequiredMixin):#loginreqmixin sub class
    """Custom mixin that requires auth and returns user profile as need """
   
    def get_profile(self): 
        """ get profile of current user"""
        return Profile.objects.get(user=self.request.user)
    
    def get_login_url(self):
        return reverse('login')

    
    def is_owner(self, profile):
        '''check user is user of current profile being viewed'''
        return self.request.user.is_authenticated and profile.user == self.request.user
    
#profile views
class ProfileDetailView(ProfileRequiredMixin, DetailView):
    '''get profile of current user'''
    model = Profile
    template_name = 'project/show_profile.html'
    context_object_name = 'profile'

    def get_object(self):
        return self.get_profile()

class UpdateProfileView(ProfileRequiredMixin, UpdateView):
    '''allow users to update profile information'''
    model = Profile
    form_class= UpdateProfileForm
    template_name = "project/update_profile_form.html"

    def get_object(self):
        return self.get_profile()

    def get_context_data(self, **kwargs):
        '''return the dict of context variables for use in the template'''
        
        context = super().get_context_data(**kwargs)

        # add to ctxt data, used to display page specific nav icons
        context['back_url'] = reverse('profile')
        
        return context

class CreateProfileView(CreateView):
    '''view to handle profile creation + user signup'''

    model = Profile
    form_class = CreateProfileForm
    template_name = "project/create_profile_form.html"

    def form_valid(self, form):
        user_form = UserCreationForm(self.request.POST)

        if not user_form.is_valid():
            context = self.get_context_data()
            context['user_form'] = user_form
            return self.render_to_response(context)

        # create Django auth user
        new_user = user_form.save()

        # log them in immediately
        login(
            self.request,
            new_user,
            backend='django.contrib.auth.backends.ModelBackend'
        )

        # attach profile to auth user
        form.instance.user = new_user

        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        '''add user creation form to template'''
        context = super().get_context_data(**kwargs)

        if 'user_form' not in context:
            context['user_form'] = UserCreationForm()

        context['back_url'] = reverse('login')
        return context

    def get_success_url(self):
        '''send user to their profile page'''
        return reverse('profile')
    

#adventure views
class AdventureListView(ProfileRequiredMixin, ListView):
    '''show all adventures created by this profile'''

    model = Adventure
    template_name = 'project/home.html'
    context_object_name = 'adventures'

    def get_queryset(self):
        profile = self.get_profile()
        return profile.get_adventures()
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        profile = self.get_profile()

        context['profile'] = profile
        context['pfp'] = profile.profile_image
        context['cover'] = profile.cover_image
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
        profile = self.get_profile()

        context['back_url'] = reverse('home')
        context['adventure'] = adventure
        context['pfp'] = profile.profile_image 
        context['cover'] = adventure.cover_image    

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
        
        response = super().form_valid(form)

        return response


class DeleteAdventureView(ProfileRequiredMixin, DeleteView):
    ''' view to handle adventure deletion '''
    model = Adventure
    template_name = "project/delete_adventure_form.html"

    def get_context_data(self, **kwargs):
        #call super
        context = super().get_context_data(**kwargs)

        #get pk
        pk = self.kwargs['pk']
        profile = self.get_profile()

        #find comm obj
        adventure = Adventure.objects.get(pk=pk)
    
        #add to context data
        context['adventure'] = adventure
        context['back_url'] = reverse('home') 
        context['pfp'] = profile.profile_image     

        return context

    def get_success_url(self):
        ''' return to home page upon successful deletion'''
        return reverse('home')
    

#destination views
class DestinationListView(ProfileRequiredMixin, ListView):
    '''show all destinations associated with an adventure'''

    model = Destination
    template_name = 'project/destinations.html'
    context_object_name = 'destinations'

    def get_queryset(self):
        pk = self.kwargs['pk']
        adventure = Adventure.objects.get(pk=pk)
        return adventure.get_destinations()
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        pk = self.kwargs['pk']
        adventure = Adventure.objects.get(pk=pk)
        profile = self.get_profile()

        context['pfp'] = profile.profile_image
        context['adventure'] = adventure
        context['back_url'] = reverse('adventure', args=[adventure.pk]) #back to the adventure page
        
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

        context['profile'] = profile
        context['cover'] = destination.cover_image
        context['back_url'] = reverse('adventure', args=[destination.adventure.pk])
        context['pfp'] = profile.profile_image
        context['destination'] = destination

        return context
    
    
class UpdateDestinationView(ProfileRequiredMixin, UpdateView):
    ''' view to handle post updates '''
    model = Destination
    form_class= UpdateDestinationForm
    template_name = "project/update_destination.html"

    def get_context_data(self, **kwargs):
        #call super
        context = super().get_context_data(**kwargs)

        #get pk
        pk = self.kwargs['pk']

        #find comm obj
        destination = Destination.objects.get(pk=pk)

        #add to context data
        context['back_url'] = reverse('destination', args=[destination.pk])
        context['destination'] = destination

        return context

    def get_success_url(self):
        ''' return to profile page upon successful deletion '''
        #find pk 
        pk = self.kwargs['pk']
        #find comm obj
        destination = Destination.objects.get(pk=pk)
        return reverse('destination', kwargs={'pk':destination.pk})
    
  
class CreateDestinationView(ProfileRequiredMixin, CreateView):
    '''view to handle adventure creation'''

    form_class = CreateDestinationForm
    template_name = 'project/create_destination.html'

    def form_valid(self,form):
        pk = self.kwargs['pk']
        adventure = Adventure.objects.get(pk=pk)

        form.instance.adventure = adventure
        return super().form_valid(form) 


class DeleteDestinationView(ProfileRequiredMixin, DeleteView):
    ''' view to handle post deletion '''
    model = Destination
    template_name = "project/delete_destination_form.html"

    def get_context_data(self, **kwargs):
        #call super
        context = super().get_context_data(**kwargs)

        #get pk
        pk = self.kwargs['pk']

        #find comm obj
        destination = Destination.objects.get(pk=pk)
    
        #add to context data
        context['destination'] = destination
        context['back_url'] = reverse('adventure', args=[destination.adventure.pk])     

        return context

    def get_success_url(self):
        ''' return to home page upon successful deletion'''
        pk = self.kwargs['pk']
        destination = Destination.objects.get(pk=pk)
        return reverse('adventure', args=[destination.adventure.pk])
    

#journal views
class JournalListView(ProfileRequiredMixin, ListView):
    '''show all journals associated with an destination'''

    model = JournalEntry
    template_name = 'project/journals.html'
    context_object_name = 'journals'

    def get_queryset(self):
        pk = self.kwargs['pk']
        destination = Destination.objects.get(pk=pk)
        return destination.get_entries()
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        pk = self.kwargs['pk']

        profile = self.get_profile()
        destination = Destination.objects.get(pk=pk)


        context['pfp'] = profile.profile_image
        context['destination'] = destination
        context['back_url'] = reverse('destination', args=[destination.pk]) #back to the destination page
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
        context['journal'] = journal
        context['back_url'] = reverse('destination', args=[journal.destination.pk])
        context['pfp'] = profile.profile_image     

        return context
    
    
class UpdateJournalView(ProfileRequiredMixin, UpdateView):
    ''' view to handle post updates '''
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
    '''view to handle destination creation'''

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


class DeleteJournalView(ProfileRequiredMixin, DeleteView):
    ''' view to handle post deletion '''
    model = JournalEntry
    template_name = "project/delete_journal_form.html"

    def get_context_data(self, **kwargs):
        #call super
        context = super().get_context_data(**kwargs)

        #get pk
        pk = self.kwargs['pk']

        #find comm obj
        journal = JournalEntry.objects.get(pk=pk)
    
        #add to context data
        context['journal'] = journal
        context['back_url'] = reverse('destination', args=[journal.destination.pk])     

        return context

    def get_success_url(self):
        ''' return to home page upon successful deletion'''
        pk = self.kwargs['pk']
        journal = JournalEntry.objects.get(pk=pk)
        return reverse('destination', args=[journal.destination.pk])
    
#transportation views
class TransportationListView(ProfileRequiredMixin, ListView):
    '''show all transportation associated with a destination'''

    model = Transportation
    template_name = 'project/transportations.html'
    context_object_name = 'transportations'

    def get_queryset(self):
        pk = self.kwargs['pk']
        destination = Destination.objects.get(pk=pk)
        return destination.get_transportation()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        pk = self.kwargs['pk']
        profile = self.get_profile()
        destination = Destination.objects.get(pk=pk)

        context['pfp'] = profile.profile_image
        context['destination'] = destination
        context['back_url'] = reverse('destination', args=[destination.pk])

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

        form.instance.destination = destination
        return super().form_valid(form)
    
class UpdateTransportationView(ProfileRequiredMixin, UpdateView):
    '''view to handle transportation updates'''

    model = Transportation
    form_class = UpdateTransportationForm
    template_name = 'project/update_transportation.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        pk = self.kwargs['pk']
        transportation = Transportation.objects.get(pk=pk)

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
    template_name = 'project/delete_transportation_form.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        pk = self.kwargs['pk']
        transportation = Transportation.objects.get(pk=pk)

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
        return destination.get_lodging()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        pk = self.kwargs['pk']
        profile = self.get_profile()
        destination = Destination.objects.get(pk=pk)

        context['pfp'] = profile.profile_image
        context['destination'] = destination
        context['back_url'] = reverse('destination', args=[destination.pk])

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

        form.instance.destination = destination
        return super().form_valid(form)
    
class UpdateLodgingView(ProfileRequiredMixin, UpdateView):
    '''view to handle lodging updates'''

    model = Lodging
    form_class = UpdateLodgingForm
    template_name = 'project/update_lodging.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        pk = self.kwargs['pk']
        lodging = Lodging.objects.get(pk=pk)

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
    template_name = 'project/delete_lodging_form.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        pk = self.kwargs['pk']
        lodging = Lodging.objects.get(pk=pk)

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
        return destination.get_activity()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        pk = self.kwargs['pk']
        profile = self.get_profile()
        destination = Destination.objects.get(pk=pk)

        context['pfp'] = profile.profile_image
        context['destination'] = destination
        context['back_url'] = reverse('destination', args=[destination.pk])

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

        form.instance.destination = destination
        return super().form_valid(form)
    
class UpdateActivityView(ProfileRequiredMixin, UpdateView):
    '''view to handle activity updates'''

    model = Activity
    form_class = UpdateActivityForm
    template_name = 'project/update_activity.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        pk = self.kwargs['pk']
        activity = Activity.objects.get(pk=pk)

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
    template_name = 'project/delete_activity_form.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        pk = self.kwargs['pk']
        activity = Activity.objects.get(pk=pk)

        context['activity'] = activity
        context['back_url'] = reverse('destination', args=[activity.destination.pk])

        return context

    def get_success_url(self):
        pk = self.kwargs['pk']
        activity = Activity.objects.get(pk=pk)
        return reverse('destination', args=[activity.destination.pk])