from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm

class LoginForm(forms.Form):
    username = forms.CharField(max_length=50, label='Login')
    password = forms.CharField(max_length=14, widget=forms.PasswordInput, label='Password')

class CreateNewAccount(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = get_user_model()
        fields = ('username',)