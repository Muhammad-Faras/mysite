from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import get_user_model

CustomUser = get_user_model()


class UserCreationFormExtended(UserCreationForm):
    
    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'password1', 'password2')
        
class AuthenticationFormExtended(AuthenticationForm):
    """
    Extend the default AuthenticationForm to customize labels.
    """
    email = forms.EmailField(label=("Email"), max_length=254)
    password = forms.CharField(label=("Password"), strip=False, widget=forms.PasswordInput)

    class Meta:
        fields = ('email', 'password')
