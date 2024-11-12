from django.shortcuts import render
from django.views.generic import DetailView, ListView
import plotly.express as px
from django.db.models import Q
from collections import Counter
from django.db.models import Count
from .models import Voter
from datetime import datetime
from django.core.paginator import Paginator
from .forms import VoterFilterForm

# Create your views here.

from django.db.models import F

class VoterListView(ListView):
    model = Voter
    template_name = 'voter_analytics/voter_list.html'
    context_object_name = 'voters'
    paginate_by = 100

    def get_queryset(self):
        queryset = super().get_queryset()

        # Initialize the filter form with GET data
        form = VoterFilterForm(self.request.GET)
        if form.is_valid():
            if form.cleaned_data['party_affiliation']:
                # Strip spaces from party affiliation for accurate filtering
                party_affiliation = form.cleaned_data['party_affiliation'].strip()
                queryset = queryset.filter(party_affiliation__icontains=party_affiliation)
            # Apply other filters as usual
            if form.cleaned_data['voter_score']:
                queryset = queryset.filter(voter_score=form.cleaned_data['voter_score'])
            if form.cleaned_data['min_dob']:
                queryset = queryset.filter(date_of_birth__gte=form.cleaned_data['min_dob'])
            if form.cleaned_data['max_dob']:
                queryset = queryset.filter(date_of_birth__lte=form.cleaned_data['max_dob'])
            if form.cleaned_data['v20state']:
                queryset = queryset.filter(v20state=True)
            if form.cleaned_data['v21town']:
                queryset = queryset.filter(v21town=True)
            if form.cleaned_data['v21primary']:
                queryset = queryset.filter(v21primary=True)
            if form.cleaned_data['v22general']:
                queryset = queryset.filter(v22general=True)
            if form.cleaned_data['v23town']:
                queryset = queryset.filter(v23town=True)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        form = VoterFilterForm(self.request.GET)  # Pass form data to the template
        context['form'] = form
        return context

class VoterDetailView(DetailView):
    model = Voter
    template_name = 'voter_analytics/voter_detail.html'
    context_object_name = 'voter'

class GraphListView(ListView):
    model = Voter
    template_name = 'voter_analytics/graphs.html'
    context_object_name = 'voters'

    def get_queryset(self):
        queryset = super().get_queryset()
        form = VoterFilterForm(self.request.GET)
        if form.is_valid():
            if form.cleaned_data['party_affiliation']:
                # Strip spaces from party affiliation for accurate filtering
                party_affiliation = form.cleaned_data['party_affiliation'].strip()
                queryset = queryset.filter(party_affiliation__icontains=party_affiliation)
            if form.cleaned_data['voter_score']:
                queryset = queryset.filter(voter_score=form.cleaned_data['voter_score'])
            if form.cleaned_data['min_dob']:
                queryset = queryset.filter(date_of_birth__gte=form.cleaned_data['min_dob'])
            if form.cleaned_data['max_dob']:
                queryset = queryset.filter(date_of_birth__lte=form.cleaned_data['max_dob'])
            if form.cleaned_data['v20state']:
                queryset = queryset.filter(v20state=True)
            if form.cleaned_data['v21town']:
                queryset = queryset.filter(v21town=True)
            if form.cleaned_data['v21primary']:
                queryset = queryset.filter(v21primary=True)
            if form.cleaned_data['v22general']:
                queryset = queryset.filter(v22general=True)
            if form.cleaned_data['v23town']:
                queryset = queryset.filter(v23town=True)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        form = VoterFilterForm(self.request.GET)
        context['form'] = form

        voters = self.get_queryset()

        # Graph 1: Voters by Year of Birth
        voters_by_year = voters.values('date_of_birth__year').annotate(count=Count('id'))
        birth_years = [entry['date_of_birth__year'] for entry in voters_by_year if entry['date_of_birth__year']]
        counts = [entry['count'] for entry in voters_by_year if entry['date_of_birth__year']]
        if birth_years and counts:
            birth_year_chart = px.bar(
                x=birth_years,
                y=counts,
                labels={'x': 'Year of Birth', 'y': 'Number of Voters'},
                title='Voters by Year of Birth'
            )
            birth_year_chart.update_layout(
                width=1000,
                height=600,
                title_font_size=24,
                xaxis_title_font_size=18,
                yaxis_title_font_size=18
            )
            context['birth_year_chart'] = birth_year_chart.to_html(full_html=False)
        else:
            context['birth_year_chart'] = "<p>No data available for Year of Birth</p>"

        # Graph 2: Voters by Party Affiliation
        party_counts = voters.values('party_affiliation').annotate(count=Count('id'))
        party_affiliations = [entry['party_affiliation'] for entry in party_counts if entry['party_affiliation']]
        party_values = [entry['count'] for entry in party_counts if entry['party_affiliation']]
        if party_affiliations and party_values:
            party_chart = px.pie(
                names=party_affiliations,
                values=party_values,
                title='Voters by Party Affiliation'
            )
            party_chart.update_layout(
                width=800,
                height=600,
                title_font_size=24
            )
            context['party_chart'] = party_chart.to_html(full_html=False)
        else:
            context['party_chart'] = "<p>No data available for Party Affiliation</p>"

        # Graph 3: Voter Participation in Elections
        election_data = [
            {'Election': '2020 State', 'Count': voters.filter(v20state=True).count()},
            {'Election': '2021 Town', 'Count': voters.filter(v21town=True).count()},
            {'Election': '2021 Primary', 'Count': voters.filter(v21primary=True).count()},
            {'Election': '2022 General', 'Count': voters.filter(v22general=True).count()},
            {'Election': '2023 Town', 'Count': voters.filter(v23town=True).count()},
        ]
        election_names = [entry['Election'] for entry in election_data if entry['Count'] > 0]
        election_counts = [entry['Count'] for entry in election_data if entry['Count'] > 0]
        if election_names and election_counts:
            election_chart = px.bar(
                x=election_names,
                y=election_counts,
                labels={'x': 'Election', 'y': 'Number of Voters'},
                title='Voter Participation in Elections'
            )
            election_chart.update_layout(
                width=800,
                height=600,
                title_font_size=24,
                xaxis_title_font_size=18,
                yaxis_title_font_size=18
            )
            context['election_chart'] = election_chart.to_html(full_html=False)
        else:
            context['election_chart'] = "<p>No data available for Election Participation</p>"

        return context