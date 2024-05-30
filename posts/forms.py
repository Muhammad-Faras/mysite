from .models import Post, Comment,Report
from django import forms


class PostForm(forms.ModelForm):
    
    class Meta:
        model = Post
        fields=('title','description', 'post_img')
        
        widgets = {
            'title': forms.TextInput(attrs={'class': 'mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm placeholder-gray-400 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm',
            'placeholder':f'whats in your mind?',
            'id':'title',
            'name':'title',
            }),
            'description': forms.Textarea(attrs={'class': 'mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm placeholder-gray-400 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm','rows':'5',
            'rows': '5',
            'id': 'content',
            'name': 'content',
            
            }),
            'post_img': forms.ClearableFileInput(attrs={
                'class': 'mt-1 block w-full text-sm text-gray-500 file:mr-4 file:py-2 file:px-4 file:rounded-md file:border-0 file:text-sm file:font-semibold file:bg-indigo-50 file:text-indigo-700 hover:file:bg-indigo-100',
                'id':'image',
                'name':'image'
                
            })
            
        }
        
        
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


class ReportForm(forms.ModelForm):
    class Meta:
        model = Report
        fields = ['reason', 'description', 'image']  # Include the 'image' field
        widgets = {
            'reason': forms.Select(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control'}),
            'image': forms.ClearableFileInput(attrs={'class': 'form-control-file'})  # Add widget for image field
        }
        
        