# voter_analytics/forms.py
from django import forms
from datetime import datetime


class VoterFilterForm(forms.Form):
    party_affiliation = forms.ChoiceField(
        choices=[('', 'Any'), ('D', 'Democratic'), ('R', 'Republican'), ('U', 'Unaffiliated')],
        required=False,
        label="Select Party Affiliation"
    )
    voter_score = forms.ChoiceField(
        choices=[('', 'Any')] + [(str(i), str(i)) for i in range(6)],
        required=False,
        label="Select Voter Score"
    )
    min_dob = forms.DateField(
        widget=forms.SelectDateWidget(years=range(1920, datetime.now().year + 1)),
        required=False,
        label="Min Year of Birth"
    )
    max_dob = forms.DateField(
        widget=forms.SelectDateWidget(years=range(1920, datetime.now().year + 1)),
        required=False,
        label="Max Year of Birth"
    )
    v20state = forms.BooleanField(required=False, label="Voted in 2020 State Election")
    v21town = forms.BooleanField(required=False, label="Voted in 2021 Town Election")
    v21primary = forms.BooleanField(required=False, label="Voted in 2021 Primary Election")
    v22general = forms.BooleanField(required=False, label="Voted in 2022 General Election")
    v23town = forms.BooleanField(required=False, label="Voted in 2023 Town Election")
