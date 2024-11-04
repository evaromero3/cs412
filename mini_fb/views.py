from django.urls import reverse
from django.shortcuts import get_object_or_404, redirect
from django.views.generic import View, ListView, DetailView, CreateView, UpdateView
from django.views.generic import DeleteView, UpdateView
from .models import Profile, StatusMessage, Image
from .forms import CreateProfileForm, CreateStatusMessageForm, UpdateProfileForm
from .forms import UpdateStatusMessageForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

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
class CreateProfileView(LoginRequiredMixin, CreateView):
    model = Profile
    form_class = CreateProfileForm
    template_name = 'mini_fb/create_profile_form.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if 'user_form' not in context:
            context['user_form'] = UserCreationForm()
        return context

    def form_valid(self, form):
        user_form = UserCreationForm(self.request.POST)
        if user_form.is_valid():
            user = user_form.save()  # Create and save the User
            form.instance.user = user  # Attach the User to the Profile
            return super().form_valid(form)
        else:
            # If the user form is invalid, re-render the context with errors
            return self.render_to_response(self.get_context_data(form=form, user_form=user_form))

    def get_success_url(self):
        return reverse('show_profile', args=[self.object.pk])

# View to create a new status message for the logged-in user's profile
class CreateStatusMessageView(LoginRequiredMixin, CreateView):
    model = StatusMessage
    form_class = CreateStatusMessageForm
    template_name = 'mini_fb/create_status_form.html'

    # Attach the logged-in user's Profile to the StatusMessage and handle image uploads
    def form_valid(self, form):
        profile = get_object_or_404(Profile, user=self.request.user)
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
        return reverse('show_profile', args=[self.request.user.profile.pk])

    # Adding the logged-in user's profile to context for use in the template
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['profile'] = get_object_or_404(Profile, user=self.request.user)
        return context

class UpdateProfileView(LoginRequiredMixin, UpdateView):
    model = Profile
    form_class = UpdateProfileForm
    template_name = 'mini_fb/update_profile_form.html'

    # Method to get the profile object associated with the logged-in user
    def get_object(self):
        return get_object_or_404(Profile, user=self.request.user)
    
    # Redirect to the profile page after a successful update
    def get_success_url(self):
        return reverse('show_profile', args=[self.request.user.profile.pk])

class DeleteStatusMessageView(LoginRequiredMixin, DeleteView):
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

class CreateFriendView(LoginRequiredMixin, View):
    def dispatch(self, request, *args, **kwargs):
        profile = get_object_or_404(Profile, user=self.request.user)
        other_profile = get_object_or_404(Profile, pk=self.kwargs['other_pk'])

        profile.add_friend(other_profile)

        return redirect('show_profile', pk=profile.pk)
    
class ShowFriendSuggestionsView(LoginRequiredMixin, DetailView):
    model = Profile
    template_name = 'mini_fb/friend_suggestions.html'
    context_object_name = 'profile'

    def get_object(self):
        return get_object_or_404(Profile, user=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['friend_suggestions'] = self.object.get_friend_suggestions()
        return context

class ShowNewsFeedView(LoginRequiredMixin, DetailView):
    model = Profile
    template_name = 'mini_fb/news_feed.html'
    context_object_name = 'profile'

    def get_object(self):
        return get_object_or_404(Profile, user=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        profile = self.get_object()
        context['news_feed'] = profile.get_news_feed()
        return context