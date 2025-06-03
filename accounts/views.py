from django.contrib.auth.forms import UserCreationForm
from django.views.generic import CreateView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import UpdateView  # This is the critical addition
from django.contrib.auth import get_user_model
from .models import UserPreferences
from .forms import PreferencesForm
from django.urls import reverse_lazy

User = get_user_model()

class RegisterView(CreateView):
    """User registration view"""
    form_class = UserCreationForm
    template_name = 'accounts/register.html'
    success_url = reverse_lazy('accounts:profile')

class ProfileView(LoginRequiredMixin, DetailView):
    """User profile view"""
    model = User
    template_name = 'accounts/profile.html'
    context_object_name = 'user_profile'

    def get_object(self):
        return self.request.user

class PreferencesView(LoginRequiredMixin, UpdateView):
    model = UserPreferences
    form_class = PreferencesForm
    template_name = 'accounts/preferences.html'
    success_url = reverse_lazy('accounts:preferences')

    def get_object(self):
        obj, created = UserPreferences.objects.get_or_create(user=self.request.user)
        return obj