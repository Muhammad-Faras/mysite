from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import get_user_model
from allauth.account.forms import SignupForm,LoginForm
from django.contrib.auth import get_user_model
from .models import Profile
from django.contrib import messages


CustomUser = get_user_model()

        
class SignupFormExtended(SignupForm):
    first_name = forms.CharField(
        max_length=25,
        label='First Name',
        widget=forms.TextInput(attrs={'class': 'mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm placeholder-gray-400 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm',
        'placeholder': 'Enter your first name',   
        })
    )
    last_name = forms.CharField(
        max_length=25,
        label='Last Name',
        widget=forms.TextInput(attrs={'class': 'mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm placeholder-gray-400 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm',
        'placeholder': 'Enter your last name'                              
        })
    )

    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'password1', 'password2')

    def __init__(self, *args, **kwargs):
        super(SignupFormExtended, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({'class': 'mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm placeholder-gray-400 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm'})
        self.fields['email'].widget.attrs.update({'class': 'mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm placeholder-gray-400 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm'})
        self.fields['password1'].widget.attrs.update({'class': 'mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm placeholder-gray-400 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm'})
        self.fields['password2'].widget.attrs.update({'class': 'mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm placeholder-gray-400 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm'})
    
    
    def save(self, request):
        user = super(SignupFormExtended, self).save(request)
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.save()
        return user

class CustomLoginForm(LoginForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['login'].widget.attrs.update({
            'class': 'mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm placeholder-gray-400 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm',
            'placeholder': 'Enter your email or username'
        })
        self.fields['password'].widget.attrs.update({
            'class': 'mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm placeholder-gray-400 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm',
            'placeholder': 'Enter your password'
        })
            

    def clean(self):
        cleaned_data = super().clean()
        email_or_username = cleaned_data.get('login')
        
        if not CustomUser.objects.filter(email=email_or_username).exists() and not CustomUser.objects.filter(username=email_or_username).exists():
            if self.request:
                messages.error(self.request, 'This email or username does not exist. Please enter a valid email or username.')
            raise forms.ValidationError('Invalid email or username.')
        
        return cleaned_data



class ProfileForm(forms.ModelForm):
    profile_img = forms.ImageField(label="Profile Picture")
    class Meta:
        model = Profile
        exclude = ['user']
        
        widgets = {
            'profile_img': forms.ClearableFileInput(attrs={'class': 'form-input'}),
            'university': forms.Select(attrs={'class': 'form-input'}),
            'skill': forms.Select(attrs={'class': 'form-input'}),
            'gender': forms.Select(attrs={'class': 'form-input'}),
            'age': forms.NumberInput(attrs={'class': 'form-input'}),
            'birthday': forms.DateInput(attrs={'class': 'form-input', 'type': 'date'}),
            'bio': forms.Textarea(attrs={'class': 'form-input'}),
            'twitter_link': forms.URLInput(attrs={'class': 'form-input'}),
            'facebook_link': forms.URLInput(attrs={'class': 'form-input'}),
            'github_link': forms.URLInput(attrs={'class': 'form-input'}),
        }
        
        # widgets = {
        #     'birthday': forms.DateInput(attrs={'type': 'date'}),
        # }
        
    def clean_age(self):
        age = self.cleaned_data.get('age')
        if age is not None and (age < 10 or age > 100):
            raise forms.ValidationError("Age must be between 10 and 100.")
        return age