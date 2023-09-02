from django import forms
from django.contrib.auth import get_user_model
from . import models


class NewTicketForm(forms.ModelForm):
    class Meta:
        model = models.Ticket
        fields = ["title", "description", "image"]


class NewReviewForm(forms.ModelForm):
    class Meta:
        model = models.Review
        fields = ["rating", "headline", "body"]
