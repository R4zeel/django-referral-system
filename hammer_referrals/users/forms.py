from django import forms
from django.forms import ModelForm

from .models import PhoneUser


class PhoneAuthForm(ModelForm):
    
    class Meta:
        model = PhoneUser
        fields = ('phone_number',)
