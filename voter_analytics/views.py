# File: views.py
# Author: Leigh Brown (ljbrown4@bu.edu), 3/17/2026
# Description: create the functions necessary to connect to html templates
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

        #for redirecting to the right page when filters are applied
        context['redirect'] = 'voters'

        return context

class VoterDetailView(DetailView):
    ''' showcase individual voter info'''
 
    template_name = 'voter_analytics/voter_detail.html'
    model = Voter
    context_object_name = 'v'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['back_url'] = reverse('voters')
        
        return context
    
class GraphListView(ListView):
    ''' showcase graphs related to the database'''
    template_name = 'voter_analytics/graphs.html'
    model = Voter
    context_object_name = "graphs"

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
        context = super().get_context_data(**kwargs)

        #get the filtered voters to use for the graphs
        voters = self.get_queryset()
        context['parties'] = Voter.objects.values_list('party', flat=True).distinct().order_by('party')
        context['selected_party'] = self.request.GET.get('party', '')

        context['scores'] = Voter.objects.values_list('score', flat=True).distinct().order_by('score')
        context['selected_score'] = self.request.GET.get('score', '')

        context['checked_v20'] = self.request.GET.get('v20', '')
        context['checked_v21t'] = self.request.GET.get('v21t', '')
        context['checked_v21p'] = self.request.GET.get('v21p', '')
        context['checked_v22'] = self.request.GET.get('v22', '')
        context['checked_v23'] = self.request.GET.get('v23', '')

        context['selected_min_dob'] = self.request.GET.get('min_dob', '')
        context['selected_max_dob'] = self.request.GET.get('max_dob', '')

        dates = Voter.objects.values_list('date_of_birth', flat=True)
        years = sorted({d.year for d in dates if d is not None}, reverse=True)
        context['years'] = years

        #1st bar graph
        yrs = {}

        for v in voters:
            #populate the dict for the graph with each yrs and the amt of voters that are born in it
            if v.date_of_birth:
                y = v.date_of_birth.year

                if y in yrs:
                    yrs[y] += 1
                else:
                    yrs[y] = 1
        
        xY = sorted(yrs.keys())
        yY = [yrs[y] for y in xY]
        figY = go.Bar(x=xY, y=yY)
        graphY = plotly.offline.plot({"data":[figY], "layout_title_text": "Voter Age Distribution"},
                                     auto_open=False, output_type="div")

        context['graphY'] = graphY

        #pie graph
        prty = {}

        for v in voters:
            if v.party:
                p = v.party
                if p in prty:
                    prty[v.party] += 1
                else:
                    prty[v.party] = 1

        xP = list(prty.keys())
        yP = list(prty.values())
        figP = go.Pie(labels=xP, values=yP)
        graphP = plotly.offline.plot({"data":[figP], "layout_title_text": "Voter Party Distribution"},
                                     auto_open=False, output_type="div")

        context['graphP'] = graphP

        #2nd bar graph
        xE = ['2020 State', '2021 Town', '2021 Primary', '2022 General', '2023 Town']
        yE= [ voters.filter(v20=True).count(),
            voters.filter(v21t=True).count(),
            voters.filter(v21p=True).count(),
            voters.filter(v22=True).count(),
            voters.filter(v23=True).count(),]
        
        figE = go.Bar(x=xE, y=yE)
        graphE = plotly.offline.plot({"data":[figE], "layout_title_text": "Voter Participation"},
                                     auto_open=False, output_type="div")
        
        context['graphE'] = graphE

        context['total'] = voters.count()

        #for redirecting to the right page when filters are applied
        context['redirect'] = 'graphs'
        return context
