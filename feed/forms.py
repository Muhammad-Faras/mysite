# classifications/forms.py

from django import forms
from .models import MainClassification, SubClassification

class ClassificationForm(forms.Form):
    main_classifications = forms.ModelMultipleChoiceField(queryset=MainClassification.objects.all(), widget=forms.CheckboxSelectMultiple, required=False)
    sub_classifications = forms.ModelMultipleChoiceField(queryset=SubClassification.objects.all(), widget=forms.CheckboxSelectMultiple, required=False)
