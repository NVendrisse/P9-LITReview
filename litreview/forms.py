from django import forms
from django.contrib.auth import get_user_model
from . import models
from authentification import models as auth


class NewTicketForm(forms.ModelForm):
    class Meta:
        model = models.Ticket
        fields = ["title", "description", "image"]


class NewReviewForm(forms.ModelForm):
    ticket_title = models.Ticket.title
    ticket_description = models.Ticket.description
    ticket_image = models.Ticket.image
    review_rating = models.Review.rating
    review_head = models.Review.headline
    review_body = models.Review.body
