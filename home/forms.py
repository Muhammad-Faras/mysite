from django.contrib.auth.forms import AuthenticationForm


class AuthenticationFormExtended(AuthenticationForm):
    class Meta:
        fields = ('__all__')