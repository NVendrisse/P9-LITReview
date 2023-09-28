from collections.abc import Mapping
from typing import Any
from django import forms
from django.contrib.auth import get_user_model
from django.core.files.base import File
from django.db.models.base import Model
from django.forms.utils import ErrorList
from . import models
from authentification import models as auth


class NewTicketForm(forms.ModelForm):
    class Meta:
        model = models.Ticket
        fields = ["title", "description", "image"]


class NewReviewForm(forms.ModelForm):
    class Meta:
        model = models.Review
        fields = ["headline", "rating", "body"]
