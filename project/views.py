from django.shortcuts import render
from django.views.generic import ListView, DetailView, TemplateView, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import UserCreationForm

from .models import Listing, Profile
from django.contrib.auth.models import User
from .forms import CreateProfileForm

from django.urls import reverse_lazy

# Create your views here.

class ListingListView(ListView):
    model = Listing  # The model to retrieve data from
    template_name = 'project/listing_list.html'  # Template to render the view
    context_object_name = 'listings'  # Name to use for the object list in the template

class ListingDetailView(DetailView):
    model = Listing
    template_name = 'project/listing_detail.html'
    context_object_name = 'listing'

class MyAccountView(LoginRequiredMixin, TemplateView):
    template_name = 'project/my_account.html'


### USER AUTHENTICATION ### 

class CreateProfileView(CreateView):
    model = Profile
    template_name = 'project/create_profile.html'
    form_class = CreateProfileForm
    success_url = reverse_lazy('my-account')  # Redirect after successful creation

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if 'user_form' not in context:
            context['user_form'] = UserCreationForm()  # Add UserCreationForm to the context
        return context

    def form_valid(self, form):
        # Handle the UserCreationForm
        user_form = UserCreationForm(self.request.POST)
        if user_form.is_valid():
            # Save the user
            user = user_form.save()
            # Assign the user to the profile
            profile = form.save(commit=False)
            profile.user = user
            profile.save()
            return super().form_valid(form)
        else:
            # If the UserCreationForm is invalid, re-render the form with errors
            return self.form_invalid(form)