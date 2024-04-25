from django import forms
from django.forms import ModelForm
from .models import ArticleModel

class ArticleForm(forms.ModelForm):
    class Meta:
        model = ArticleModel
        fields = ('article_title','article_body')