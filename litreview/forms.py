from django import forms
from django.contrib.auth import get_user_model
from . import models

user = get_user_model()

class SocialForm(forms.ModelForm):
    class Meta:
        model = models.UserFollows
        fields = ['followed_user']