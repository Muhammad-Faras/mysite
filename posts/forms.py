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
            'comment_body': forms.Textarea(attrs={'class': 'border rounded-full p-2', 'rows': 1, 'style': 'resize: none;'})
        }