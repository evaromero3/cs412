from django.urls import reverse
from django.shortcuts import get_object_or_404
from django.views.generic import ListView, DetailView, CreateView, UpdateView
from django.views.generic import DeleteView, UpdateView
from .models import Profile, StatusMessage, Image
from .forms import CreateProfileForm, CreateStatusMessageForm, UpdateProfileForm
from .forms import UpdateStatusMessageForm

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

    # Attach the Profile to the StatusMessage and handle image uploads
    def form_valid(self, form):
        profile = get_object_or_404(Profile, pk=self.kwargs['pk'])
        form.instance.profile = profile
        status_message = form.save()

        # Handle the uploaded files (images)
        files = self.request.FILES.getlist('files')
        for file in files:
            # Create an Image object for each file
            img = Image(status_message=status_message, image_file=file)
            img.save()

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

class UpdateProfileView(UpdateView):
    model = Profile
    form_class = UpdateProfileForm
    template_name = 'mini_fb/update_profile_form.html'

    # Redirect to the profile page after a successful update
    def get_success_url(self):
        return reverse('show_profile', args=[self.object.pk])

class DeleteStatusMessageView(DeleteView):
    model = StatusMessage
    template_name = 'mini_fb/delete_status_form.html'
    context_object_name = 'status_message'

    # After successfully deleting, redirect to the profile page
    def get_success_url(self):
        profile_pk = self.object.profile.pk  # Get the profile pk related to the status message
        return reverse('show_profile', args=[profile_pk])

class UpdateStatusMessageView(UpdateView):
    model = StatusMessage
    fields = ['message']  # Allow updating only the message field
    template_name = 'mini_fb/update_status_form.html'

    # After successfully updating, redirect back to the profile page
    def get_success_url(self):
        profile_pk = self.object.profile.pk  # Get the profile pk related to the status message
        return reverse('show_profile', args=[profile_pk])