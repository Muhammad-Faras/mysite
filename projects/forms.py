from django import forms
from .models import ProjcetShowcase
from ckeditor.widgets import CKEditorWidget
from ckeditor_uploader.widgets import CKEditorUploadingWidget
class ProjcetShowcase_Form(forms.ModelForm):
    class Meta:
        model = ProjcetShowcase
        fields = ('project_title','project_thumbnail_image', 'project_description')
        widgets = {
            'project_title': forms.TextInput(attrs={'class': 'form-control'}),
            'project_description': CKEditorWidget(attrs={'class': 'form-control no-border', 'id': 'project-description'}),
        }

        widgets = {
            'project_title': forms.TextInput(attrs={'class': 'w-full input-field rounded-lg px-4 py-3 focus:outline-none focus:border-blue-500',
            'placeholder':'Enter blog title...',
            'id':'project-title'
            }),
            'project_thumbnail_image': forms.ClearableFileInput(attrs={'class': 'w-full input-field rounded-lg px-4 py-3 focus:outline-none focus:border-blue-500',
            'placeholder':'Enter blog title...',
            "id":"blog-thumbnail",
            }),
            
            'project_description': CKEditorUploadingWidget(attrs={'class': 'w-full input-field rounded-lg px-4 py-3 focus:outline-none focus:border-blue-500',
            'placeholder':'Enter blog description...',
            }),
        }
        