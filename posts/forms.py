from .models import Post, Comment
from django import forms
from django.forms import ModelForm
class PostForm(forms.ModelForm):
    
    class Meta:
        model = Post
        fields=('title','description', 'post_img')
        
class FeedPostForm(forms.ModelForm):
    
    class Meta:
        model = Post
        fields=('title', 'post_img')
        

        widgets = {
            'title': forms.TextInput(attrs={'class': 'w-full resize-none border rounded-md py-2 px-3 focus:outline-none focus:ring focus:border-blue-300',
            'placeholder':f'whats in your mind?'
            }),
            'post_img': forms.ClearableFileInput(attrs={
                'class': 'hidden',
                'id': 'image-upload',
                
            })
            
        }
        
        
        
class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields=('comment_body',)
        
        widgets = {
            'comment_body': forms.Textarea(attrs={'class': 'border rounded-full p-2', 'rows': 1, 'style': 'resize: none;'})
        }