from django import forms
from .models import ProjcetShowcase
from ckeditor.widgets import CKEditorWidget

class ProjcetShowcase_Form(forms.ModelForm):
    class Meta:
        model = ProjcetShowcase
        fields = ('project_title', 'project_description')
        widgets = {
            'project_title': forms.TextInput(attrs={'class': 'form-control'}),
            'project_description': CKEditorWidget(attrs={'class': 'form-control no-border', 'id': 'project-description'}),
        }
