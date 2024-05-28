# forms.py
from django import forms
from .models import University, Skill

class SearchForm(forms.Form):
    university = forms.ModelChoiceField(queryset=University.objects.all(), required=False, label="University")
    skill = forms.ModelChoiceField(queryset=Skill.objects.all(), required=False, label="Skill")
    
