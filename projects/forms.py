from django import forms
from .models import ProjcetShowcase
from ckeditor.widgets import CKEditorWidget
class ProjcetShowcase_Form(forms.ModelForm):
    class Meta:
        model = ProjcetShowcase
        fields = ('project_title', 'project_description')