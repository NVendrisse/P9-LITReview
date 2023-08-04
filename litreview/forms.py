from django import forms
from django.contrib.auth import get_user_model
from . import models


class SocialForm(forms.ModelForm):
    class Meta:
        model = models.UserFollows
        fields = ['followed_user']

class NewTicketForm(forms.ModelForm):
    class Meta:
        model = models.Ticket
        fields = ['title', 'description', 'image']

class NewReviewForm(forms.ModelForm):
    class Meta:
        model = models.Review
        fields = ['ticket', 'rating', 'headline', 'body']
