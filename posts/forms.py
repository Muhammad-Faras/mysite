from .models import Post, Comment,Report
from django import forms

    
class FeedPostForm(forms.ModelForm):
    
    class Meta:
        model = Post
        fields=('title','description', 'post_img')
        

        widgets = {
            'title': forms.TextInput(attrs={'class': 'w-full mb-2   border rounded-md py-2 px-3 focus:outline-none focus:ring focus:border-blue-300',
            'placeholder':f'whats in your mind?'
            }),
            'description': forms.Textarea(attrs={'class': 'w-full  mb-2  border rounded-md py-2 px-3 focus:outline-none focus:ring focus:border-blue-300',
            'rows': 2,
            'cols': 2,
            'placeholder':f'description'
            }),
            'post_img': forms.ClearableFileInput(attrs={
                'class': 'hidden',
                'id': 'image-upload',
                
            })
            
        }
        
        
        
class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['comment_body']
        widgets = {
            'comment_body': forms.Textarea(attrs={
            'class': 'w-full resize-none border rounded-md py-2 px-3 focus:outline-none focus:ring focus:border-blue-300',
            'rows': '1',
            'id':"comment",
            'placeholder': 'Enter your comment here...'
        }),
            
}   
        

class ReportForm(forms.ModelForm):
    class Meta:
        model = Report
        fields = ['reason', 'description', 'image']
        widgets = {
            'reason': forms.Select(attrs={'class': 'form-select mt-1 block w-full'}),
            'description': forms.Textarea(attrs={'class': 'form-textarea mt-1 block w-full'}),
            'image': forms.ClearableFileInput(attrs={'class': 'form-file-input mt-1 block w-full'})
        }
        