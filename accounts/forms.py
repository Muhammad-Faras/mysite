from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import get_user_model
from allauth.account.forms import SignupForm
from allauth.account.forms import SignupForm
from django.contrib.auth import get_user_model
from .models import Profile



CustomUser = get_user_model()

class SignupFormExtended(SignupForm):
    first_name = forms.CharField(max_length=25, label='First Name')
    last_name = forms.CharField(max_length=25, label='Last Name')

    def save(self, request):
        user = super(SignupFormExtended, self).save(request)
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.save()
        return user
    # Add any customizations or additional fields here if needed
    class Meta:
        model = CustomUser
        fields = ('username','email', 'password1', 'password2')

        
class AuthenticationFormExtended(AuthenticationForm):
    """
    Extend the default AuthenticationForm to customize labels.
    """
    email = forms.EmailField(label=("Email"), max_length=254)
    password = forms.CharField(label=("Password"), strip=False, widget=forms.PasswordInput)

    class Meta:
        fields = ('email', 'password')




class ProfileForm(forms.ModelForm):
    profile_img = forms.ImageField(label="Profile Picture")
    class Meta:
        model = Profile
        exclude = ['user']
        widgets = {
            'birthday': forms.DateInput(attrs={'type': 'date'}),
        }
        
    def clean_age(self):
        age = self.cleaned_data.get('age')
        if age is not None and (age < 10 or age > 100):
            raise forms.ValidationError("Age must be between 10 and 100.")
        return age