from django import forms
from django.forms import ModelForm
from .models import ArticleModel

class ArticleForm(forms.ModelForm):
    class Meta:
        model = ArticleModel
        fields = ('article_title', 'article_thumbnail_image', 'article_description', 'article_body')
        
        widgets = {
            'article_title': forms.TextInput(attrs={'class': 'w-full input-field rounded-lg px-4 py-3 focus:outline-none focus:border-blue-500',
            'placeholder':'Enter blog title...',
            }),
            'article_description': forms.Textarea(attrs={'class': 'w-full', 'rows': 4,
            'placeholder':'Enter blog description...',
            }),
        }