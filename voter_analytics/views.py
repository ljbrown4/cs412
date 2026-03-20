from django.shortcuts import render
from django.urls import reverse
from django.views.generic import ListView, DetailView
from . models import *
import plotly
import plotly.graph_objs as go

# Create your views here.

class VotersListView(ListView):
    '''View to display marathon results'''
 
    template_name = 'voter_analytics/voters.html'
    model = Voter
    context_object_name = 'voters'
    paginate_by = 100 # how many records per page
 
    def get_queryset(self):
        voters = super().get_queryset().order_by('last_name')

        # filter by party
        if 'party' in self.request.GET:
            party = self.request.GET['party']
            if party:
                voters = voters.filter(party=party)

        # filter by score
        score = self.request.GET.get('score')
        if score:
            voters = voters.filter(score=score)

        #filter by year
        # minimum year
        min_dob = self.request.GET.get('min_dob')
        if min_dob:
            voters = voters.filter(date_of_birth__year__gte=min_dob)

        # maximum year
        max_dob = self.request.GET.get('max_dob')
        if max_dob:
            voters = voters.filter(date_of_birth__year__lte=max_dob)

        # filter by elections
        if self.request.GET.get('v20'):
            voters = voters.filter(v20=True)

        if self.request.GET.get('v21t'):
            voters = voters.filter(v21t=True)

        if self.request.GET.get('v21p'):
            voters = voters.filter(v21p=True)

        if self.request.GET.get('v22'):
            voters = voters.filter(v22=True)

        if self.request.GET.get('v23'):
            voters = voters.filter(v23=True)

        return voters
    
    def get_context_data(self, **kwargs):
        ''' to allow different options for filtering'''
        context = super().get_context_data(**kwargs)

        #looked up how to get a specific column from a record using object manager

        #party (options and chosen)
        context['parties'] = Voter.objects.values_list('party', flat=True).distinct().order_by('party')
        context['selected_party'] = self.request.GET.get('party', '')
        #voter score (options and chosen)
        context['scores'] = Voter.objects.values_list('score', flat=True).distinct().order_by('score')
        context['selected_score'] = self.request.GET.get('score', '')
        #elections (checkboxes)
        context['checked_v20'] = self.request.GET.get('v20', '')
        context['checked_v21t'] = self.request.GET.get('v21t', '')
        context['checked_v21p'] = self.request.GET.get('v21p', '')
        context['checked_v22'] = self.request.GET.get('v22', '')
        context['checked_v23'] = self.request.GET.get('v23', '')

        #birth
        context['selected_min_dob'] = self.request.GET.get('min_dob', '')
        context['selected_max_dob'] = self.request.GET.get('max_dob', '')

        dates = Voter.objects.values_list('date_of_birth', flat=True)

        years = sorted({ d.year for d in dates if d is not None}, reverse=True) #get the range of birthdays

        context['years'] = years

        context['total'] = self.get_queryset().count() #get the total number of records being showcased

        #Looked up online how to make filtered results stay when you hit next
        querydict = self.request.GET.copy()
        if 'page' in querydict:
            del querydict['page']
        context['filters'] = querydict.urlencode()

        return context

class VoterDetailView(DetailView):
    ''''''
 
    template_name = 'voter_analytics/voter_detail.html'
    model = Voter
    context_object_name = 'v'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['back_url'] = reverse('voters')
        
        return context

