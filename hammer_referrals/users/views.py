from typing import Any
from django.shortcuts import render
from django.urls import reverse
from django.views.generic.edit import CreateView, FormView
from django.views.generic import ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import authenticate, login

from .models import PhoneUser
from .forms import PhoneAuthForm


class UserCreateView(FormView):
    form_class = PhoneAuthForm
    template_name = 'users/registration_form.html'
    
    def get_success_url(self) -> str:
        return reverse('users:profile', kwargs={'username': self.request.user})
    

class PhoneVerifyView(CreateView):
    pass


class UserProfileView(ListView):
    template_name = 'users/profile.html'
    model = PhoneUser

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['profile'] = self.request.user
        return context
