from django.urls import reverse
from django.shortcuts import get_object_or_404
from django.views.generic import ListView, DetailView, CreateView
from .models import Profile, StatusMessage
from .forms import CreateProfileForm, CreateStatusMessageForm

# View to show all profiles
class ShowAllProfilesView(ListView):
    model = Profile
    template_name = 'mini_fb/show_all_profiles.html'
    context_object_name = 'profiles'

# View to show a single profile page
class ShowProfilePageView(DetailView):
    model = Profile
    template_name = 'mini_fb/show_profile.html'
    context_object_name = 'profile'

# View to create a new profile
class CreateProfileView(CreateView):
    model = Profile
    form_class = CreateProfileForm
    template_name = 'mini_fb/create_profile_form.html'

    # After successfully creating a profile, redirect to the profile page
    def get_success_url(self):
        return reverse('show_profile', args=[self.object.pk])

# View to create a new status message for a specific profile
class CreateStatusMessageView(CreateView):
    model = StatusMessage
    form_class = CreateStatusMessageForm
    template_name = 'mini_fb/create_status_form.html'

    # Attach the Profile to the StatusMessage
    def form_valid(self, form):
        profile = get_object_or_404(Profile, pk=self.kwargs['pk'])
        form.instance.profile = profile
        return super().form_valid(form)

    # After successfully posting a status, redirect back to the profile page
    def get_success_url(self):
        profile_pk = self.kwargs['pk']  # Pass the profile pk correctly
        return reverse('show_profile', args=[profile_pk])

    # Adding profile to context for use in the template
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['profile'] = get_object_or_404(Profile, pk=self.kwargs['pk'])
        return context
