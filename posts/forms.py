from .models import Post, Comment
from django import forms
from django.forms import ModelForm
class PostForm(forms.ModelForm):
    
    class Meta:
        model = Post
        fields=('title','description', 'post_img')
        
        
class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields=('comment_body',)
        
        widgets = {
            'comment_body': forms.Textarea(attrs={'rows': 4}),  # Customize widget for comment body
        }