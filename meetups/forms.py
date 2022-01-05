from django import forms
from django.forms import models

from .models import Participant

class RegistrationForm(forms.ModelForm):
    class Meta:
        model = Participant
        fields = ['email', ]