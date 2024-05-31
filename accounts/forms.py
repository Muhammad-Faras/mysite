from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import get_user_model
from allauth.account.forms import SignupForm,LoginForm
from django.contrib.auth import get_user_model
from .models import Profile,Skill
from django.contrib import messages
from django.shortcuts import render, get_object_or_404
from django import forms
CustomUser = get_user_model()
from .models import Skill, SubSkill

class MainSkillForm(forms.ModelForm):
    class Meta:
        model = Skill
        fields = ['skill_name']

class SubSkillForm(forms.ModelForm):
    class Meta:
        model = SubSkill
        fields = ['name', 'main_skill']
        widgets = {
            'main_skill': forms.HiddenInput()
        }

from django.core.validators import EmailValidator, RegexValidator, MinLengthValidator, MaxLengthValidator
from django.core.exceptions import ValidationError
import re
# Custom validator for alphanumeric username with letters and numbers
def validate_custom_username(value):
    if not value.isalnum():
        raise ValidationError('Username must be alphanumeric')
    if len(value) < 4:
        raise ValidationError('Username must be at least 4 characters long')
    if not re.search(r'[A-Za-z]', value):
        raise ValidationError('Username must contain at least one letter')
    if not re.search(r'\d', value):
        raise ValidationError('Username must contain at least one number')
# Custom validator for first and last name
def validate_name(value):
    if not value.isalpha():
        raise ValidationError(
            'Name must contain only letters'
        )
    if len(value) < 4:
        raise ValidationError(
            'Name must be at least 4 characters long'
        )
    if len(value) > 16:
        raise ValidationError(
            'Name must be less than 16 characters long'
        )

class SignupFormExtended(SignupForm):
    first_name = forms.CharField(
        min_length=4,
        max_length=18,
        label='First Name',
        validators=[validate_name],
        widget=forms.TextInput(attrs={
            'class': 'mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm placeholder-gray-400 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm',
            'placeholder': 'Enter your first name',   
        })
    )
    last_name = forms.CharField(
        min_length=4,
        max_length=18,
        label='Last Name',
        validators=[validate_name],
        widget=forms.TextInput(attrs={
            'class': 'mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm placeholder-gray-400 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm',
            'placeholder': 'Enter your last name'                              
        })
    )
    username = forms.CharField(
        min_length=4,
        max_length=18,
        label='Username',
        help_text='username must contain both letters and numbers',
        validators=[validate_custom_username],
        widget=forms.TextInput(attrs={
            'class': 'mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm placeholder-gray-400 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm',
            'placeholder': 'Enter your username'
        })
    )
    email = forms.EmailField(
        label='Email',
        help_text='Enter a valid @gmail.com email address.',
        validators=[EmailValidator(message="Enter a valid @gmail.com email address")],
        widget=forms.EmailInput(attrs={
            'class': 'mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm placeholder-gray-400 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm',
            'placeholder': 'Enter your email'
        })
    )
    password1 = forms.CharField(
        label='Password',
        strip=False,
        validators=[MinLengthValidator(8), MaxLengthValidator(18)],
        widget=forms.PasswordInput(attrs={
            'class': 'mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm placeholder-gray-400 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm',
            'placeholder': 'Enter your password'
        })
    )
    password2 = forms.CharField(
        label='Password confirmation',
        widget=forms.PasswordInput(attrs={
            'class': 'mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm placeholder-gray-400 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm',
            'placeholder': 'Confirm your password'
        }),
        strip=False,
        validators=[MinLengthValidator(8), MaxLengthValidator(18)]
    )

    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'password1', 'password2', 'first_name', 'last_name')

    def __init__(self, *args, **kwargs):
        super(SignupFormExtended, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({
            'class': 'mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm placeholder-gray-400 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm'
        })
        self.fields['email'].widget.attrs.update({
            'class': 'mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm placeholder-gray-400 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm'
        })
        self.fields['password1'].widget.attrs.update({
            'class': 'mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm placeholder-gray-400 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm'
        })
        self.fields['password2'].widget.attrs.update({
            'class': 'mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm placeholder-gray-400 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm'
        })
    
    def save(self, request):
        user = super(SignupFormExtended, self).save(request)
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.save()
        return user
    
# class SignupFormExtended(SignupForm):
#     first_name = forms.CharField(
#         max_length=25,
#         label='First Name',
#         widget=forms.TextInput(attrs={'class': 'mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm placeholder-gray-400 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm',
#         'placeholder': 'Enter your first name',   
#         })
#     )
#     last_name = forms.CharField(
#         max_length=25,
#         label='Last Name',
#         widget=forms.TextInput(attrs={'class': 'mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm placeholder-gray-400 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm',
#         'placeholder': 'Enter your last name'                              
#         })
#     )

#     class Meta:
#         model = CustomUser
#         fields = ('username', 'email', 'password1', 'password2')

#     def __init__(self, *args, **kwargs):
#         super(SignupFormExtended, self).__init__(*args, **kwargs)
#         self.fields['username'].widget.attrs.update({'class': 'mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm placeholder-gray-400 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm'})
#         self.fields['email'].widget.attrs.update({'class': 'mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm placeholder-gray-400 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm'})
#         self.fields['password1'].widget.attrs.update({'class': 'mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm placeholder-gray-400 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm'})
#         self.fields['password2'].widget.attrs.update({'class': 'mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm placeholder-gray-400 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm'})
    
    
#     def save(self, request):
#         user = super(SignupFormExtended, self).save(request)
#         user.first_name = self.cleaned_data['first_name']
#         user.last_name = self.cleaned_data['last_name']
#         user.save()
#         return user

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
            'profile_img': forms.ClearableFileInput(attrs={'class': 'mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm placeholder-gray-400 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm'}),
            'university': forms.Select(attrs={'class': 'mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm placeholder-gray-400 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm'}),
            'skill': forms.Select(attrs={'class': 'mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm placeholder-gray-400 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm'}),
            'gender': forms.Select(attrs={'class': 'mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm placeholder-gray-400 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm'}),
            'birthday': forms.DateInput(attrs={'class': 'mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm placeholder-gray-400 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm', 'type': 'date'}),
            'bio': forms.Textarea(attrs={'class': 'mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm placeholder-gray-400 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm'}),
        }
        
        # widgets = {
        #     'birthday': forms.DateInput(attrs={'type': 'date'}),
        # }
        
    # def clean_age(self):
    #     age = self.cleaned_data.get('age')
    #     if age is not None and (age < 10 or age > 100):
    #         raise forms.ValidationError("Age must be between 10 and 100.")
    #     return age






# class StudentProfileForm(forms.ModelForm):
#     class Meta:
#         model = StudentSkill
#         fields = ('skill',)
#         widgets = {
#             'skill': forms.RadioSelect(attrs={'class':'bcolor'}),
#         }
    

# class SubSkillForm(forms.Form):
#     def __init__(self, *args, **kwargs):
#         student_skill_id = kwargs.pop('student_skill_id', None)
#         super(SubSkillForm, self).__init__(*args, **kwargs)
#         if student_skill_id:
#             self.fields['sub_skills'] = forms.ModelMultipleChoiceField(
#                 queryset=StudentSubSkill.objects.filter(main_skill=StudentSkill.objects.filter),
#                 widget=forms.CheckboxSelectMultiple,
#                 required=False
#             )